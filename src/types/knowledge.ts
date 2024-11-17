export interface KnowledgeBase {
  name: string
  description: string
  space_name: string
  api_url: string
  model: string
}

export interface KnowledgeBaseResponse {
  choices: {
    delta: {
      content: string
    }
  }[]
}

export interface MessageReference {
  content: string
  source: string
  similarity: number
}

export interface ChatMessage {
  sender: 'user' | 'ai'
  content: string
  feedback: 'positive' | 'negative' | null
  references?: MessageReference[]
} 