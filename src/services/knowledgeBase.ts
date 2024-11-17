import axios from 'axios'
import type { KnowledgeBase, KnowledgeBaseResponse } from '@/types/knowledge'

// 添加响应类型
interface StreamChunk {
  type: 'content' | 'reference'
  text: string
  source?: string
  similarity?: number
}

export class KnowledgeBaseService {
  // 测试知识库连接
  static async testConnection(kb: KnowledgeBase): Promise<boolean> {
    try {
      const response = await axios.post(
        kb.api_url,
        {
          messages: "测试连接",
          model: kb.model,
          chat_mode: "chat_knowledge", 
          chat_param: kb.space_name
        },
        {
          headers: {
            "Authorization": "Bearer dbgpt",
            "Content-Type": "application/json"
          },
          timeout: 5000
        }
      )
      return response.status === 200
    } catch (error) {
      console.error('Knowledge base connection test failed:', error)
      throw error
    }
  }

  // 发送知识库查询 - 使用流式响应
  static async query(kb: KnowledgeBase, message: string) {
    const response = await fetch(kb.api_url, {
      method: 'POST',
      headers: {
        "Authorization": "Bearer dbgpt",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        messages: message,
        model: kb.model,
        chat_mode: "chat_knowledge",
        chat_param: kb.space_name
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No readable stream available')
    }

    // 使用 Map 而不是 Set 来记录引用，可以存储更多信息
    const processedRefs = new Map()
    let currentContent = ''

    return {
      async *[Symbol.asyncIterator](): AsyncIterator<StreamChunk> {
        try {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            const text = new TextDecoder().decode(value)
            const lines = text.split('\n')
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(5)
                if (data === '[DONE]') return
                
                try {
                  const parsed = JSON.parse(data)
                  // 处理回答内容
                  if (parsed.choices?.[0]?.delta?.content) {
                    currentContent += parsed.choices[0].delta.content
                    yield {
                      type: 'content',
                      text: parsed.choices[0].delta.content
                    }
                  }
                  // 处理引用内容
                  if (parsed.references) {
                    // 清理之前的引用记录，只保留当前回答相关的引用
                    if (currentContent.includes('<references')) {
                      processedRefs.clear()
                    }
                    
                    // 遍历所有引用块
                    for (const ref of parsed.references) {
                      for (const chunk of ref.chunks) {
                        // 使用更可靠的唯一标识
                        const refKey = `${chunk.id}-${chunk.content.substring(0, 50)}`
                        
                        if (!processedRefs.has(refKey)) {
                          processedRefs.set(refKey, {
                            content: chunk.content,
                            source: chunk.meta_info?.source || '未知',
                            similarity: chunk.recall_score
                          })
                          
                          yield {
                            type: 'reference',
                            text: chunk.content,
                            source: chunk.meta_info?.source || '未知',
                            similarity: chunk.recall_score,
                            id: chunk.id
                          }
                        }
                      }
                    }
                  }
                } catch (e) {
                  console.error('Failed to parse JSON:', e)
                }
              }
            }
          }
        } finally {
          reader.releaseLock()
        }
      }
    }
  }
} 