<template>
  <div class="flex flex-col h-screen bg-gradient-to-br from-slate-900 to-slate-800">
    <header class="flex items-center p-4 bg-slate-800">
      <div class="flex items-center flex-grow">
        <h1 class="text-2xl font-bold flex items-center text-emerald-400">
          <Cpu class="mr-2" :size="24" />
          GAMECO HR员工服务知识库
        </h1>

        <div class="flex items-center ml-8 space-x-8 text-emerald-300">
          <div class="flex items-center space-x-2">
            <Brain class="w-5 h-5 animate-pulse" />
            <span class="text-sm font-medium">智能问答</span>
          </div>
          <div class="flex items-center space-x-2">
            <Zap class="w-5 h-5 animate-bounce" />
            <span class="text-sm font-medium">创新服务</span>
          </div>
          <div class="flex items-center space-x-2">
            <Database class="w-5 h-5 animate-spin-slow" />
            <span class="text-sm font-medium">探索优化</span>
          </div>
        </div>
      </div>

      <div class="flex gap-4">
        <button 
          @click="openSettings" 
          class="text-slate-400 hover:text-emerald-400 transition-colors" 
          aria-label="设置"
        >
          <Settings :size="20" />
        </button>
        <!-- <button 
          class="text-slate-400 hover:text-emerald-400 transition-colors" 
          aria-label="返回主页"
        >
          <Home :size="20" />
        </button> -->
        <!-- <button 
          class="text-slate-400 hover:text-slate-100 transition-colors" 
          aria-label="关闭"
        >
          <X :size="20" />
        </button> -->
      </div>
    </header>

    <main ref="mainContent" class="flex-grow overflow-y-auto p-6 space-y-4" @scroll="handleScroll">
      <div v-if="showCategories" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <div v-for="(category, index) in categories" 
             :key="category.name" 
             class="bg-slate-800 rounded-lg p-4 transition-all duration-300 cursor-pointer transform hover:scale-105"
             :class="[
               selectedCardIndex === index 
                 ? 'ring-2 ring-emerald-500 shadow-lg shadow-emerald-500/20 bg-slate-700' 
                 : 'hover:bg-slate-700',
               currentKnowledgeBase?.name === category.name 
                 ? 'ring-2 ring-emerald-500 shadow-lg shadow-emerald-500/20 bg-slate-700'
                 : ''
             ]"
             @click="selectCategory(category, index)"
        >
          <h3 class="text-lg font-semibold mb-2 flex items-center text-emerald-400">
            <component :is="category.icon" class="mr-2" :size="18" />
            {{ category.name }}
            <span v-if="currentKnowledgeBase?.name === category.name" 
                  class="ml-2 text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full">
              已选择
            </span>
          </h3>
          <p class="text-slate-300">{{ category.description }}</p>
        </div>
      </div>
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>
      
      <div class="space-y-4">
        <div v-for="(message, index) in chatHistory" :key="index" class="flex items-start space-x-2 group">
          <Bot v-if="message.sender === 'ai'" :class="isEnhancedMode ? 'text-fuchsia-400' : 'text-emerald-400'" class="w-8 h-8 mt-1" />
          <User v-else :class="isEnhancedMode ? 'text-fuchsia-400' : 'text-emerald-400'" class="w-8 h-8 mt-1" />
          <div
            v-if="message.sender === 'ai'"
            class="rounded-lg p-4 shadow-lg max-w-3xl relative overflow-hidden group bg-slate-700"
          >
            <div class="prose prose-invert max-w-none">
              <div class="markdown-content mb-4 text-slate-50"
                   v-html="renderContent(message.content)"
              ></div>
            </div>

            <div v-if="showReferences && getReferences(message).length > 0" class="mt-4 pt-4 border-t border-gray-600/30">
              <div class="flex flex-wrap gap-2">
                <div v-for="(chunk, index) in getReferences(message)" 
                     :key="index"
                     class="relative group/ref inline-block"
                >
                  <span 
                    class="reference-tag inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium cursor-pointer transition-all duration-200 bg-slate-600/60 hover:bg-slate-500/80 text-slate-100"
                    @mouseenter="showPopup($event, index)"
                    @mouseleave="hidePopup"
                  >
                    <Book class="w-3 h-3 mr-1.5" />
                    引用 {{ index + 1 }}
                    <span class="ml-1.5 px-1.5 py-0.5 bg-white/10 rounded-full text-xs">
                      {{ Math.round(chunk.recall_score * 100) }}%
                    </span>
                  </span>

                  <Transition
                    enter-active-class="transition duration-200 ease-out"
                    enter-from-class="opacity-0 scale-95"
                    enter-to-class="opacity-100 scale-100"
                    leave-active-class="transition duration-150 ease-in"
                    leave-from-class="opacity-100 scale-100"
                    leave-to-class="opacity-0 scale-95"
                  >
                    <div v-if="activePopupIndex === index && isPopupVisible"
                         ref="popup"
                         class="reference-popup fixed z-[9999] w-96 max-w-[calc(100vw-2rem)]"
                         :style="popupPosition"
                         @mouseenter="keepPopup = true"
                         @mouseleave="keepPopup = false"
                    >
                      <div class="p-4 rounded-lg shadow-xl overflow-auto bg-slate-800/95 backdrop-blur-sm border border-slate-600/30"
                           :style="{ maxHeight: 'calc(100vh - 100px)' }"
                      >
                        <div class="text-sm leading-relaxed custom-scrollbar text-slate-50">
                          {{ chunk.content }}
                        </div>
                        <div class="mt-3 pt-3 border-t border-gray-600/30 flex items-center justify-between text-xs text-gray-400">
                          <span>来源: {{ chunk.meta_info?.source || '未知' }}</span>
                          <span class="flex items-center">
                            相关度
                            <span class="ml-1 px-2 py-0.5 rounded-full" 
                                  :class="getScoreClass(chunk.recall_score)">
                              {{ Math.round(chunk.recall_score * 100) }}%
                            </span>
                          </span>
                        </div>
                      </div>
                      <div class="absolute w-4 h-4 transform rotate-45 bg-slate-800"
                           :style="arrowPosition"
                      ></div>
                    </div>
                  </Transition>
                </div>
              </div>
            </div>

            <button
              @click="copyToClipboard(message.content, index)"
              class="absolute top-2 right-2 bg-gray-700 hover:bg-gray-600 text-white rounded px-2 py-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-200"
            >
              {{ copiedIndex === index ? '已复制' : '复制' }}
            </button>
          </div>
          <div v-if="message.sender === 'ai'" class="flex flex-col items-center ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button
              @click="provideFeedback(index, 'positive')"
              class="text-green-500 hover:text-green-400 mb-2"
              :class="{ 'opacity-50': message.feedback === 'positive' }"
              :disabled="message.feedback === 'positive'"
            >
              <ThumbsUp :size="18" />
            </button>
            <button
              @click="provideFeedback(index, 'negative')"
              class="text-red-500 hover:text-red-400"
              :class="{ 'opacity-50': message.feedback === 'negative' }"
              :disabled="message.feedback === 'negative'"
            >
              <ThumbsDown :size="18" />
            </button>
          </div>
          <div v-else
            class="rounded-lg p-4 shadow-lg max-w-3xl relative overflow-hidden"
            :class="isEnhancedMode 
              ? 'bg-fuchsia-800/50 backdrop-blur-sm border border-indigo-500/50 shadow-indigo-500/20' 
              : 'bg-slate-600'"
          >
            <div class="prose prose-invert max-w-none">
              <div :class="isEnhancedMode ? 'text-fuchsia-50' : 'text-slate-50'"
                   v-html="renderContent(message.content)"
              ></div>
            </div>
            <button
              @click="copyToClipboard(message.content, index)"
              class="absolute top-2 right-2 bg-gray-700 hover:bg-gray-600 text-white rounded px-2 py-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-200"
            >
              {{ copiedIndex === index ? '已复制' : '复制' }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <footer class="p-4 bg-slate-800">
      <div class="flex gap-2 mb-2">
        <button
          v-if="isGenerating"
          @click="stopGeneration"
          class="flex-1 py-2 px-4 rounded-md bg-red-600 hover:bg-red-700 text-white transition duration-200 ease-in-out"
        >
          <span class="relative z-10 flex items-center justify-center">
            <Square :size="18" class="mr-2" />
            停止生成
          </span>
        </button>
        <button
          @click="clearChat"
          class="flex-1 py-2 px-4 rounded-md bg-slate-600 hover:bg-slate-700 text-white transition duration-200 ease-in-out"
        >
          <Eraser :size="18" class="inline mr-2" />
          清除对话
        </button>
        <button
          @click="toggleCategories"
          class="flex-1 py-2 px-4 rounded-md bg-slate-600 hover:bg-slate-700 text-white transition duration-200 ease-in-out"
        >
          <BookOpen :size="18" class="inline mr-2" />
          {{ showCategories ? '收起目录' : '展开目录' }}
        </button>
      </div>
      <div class="flex relative">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="输入您的问题..."
          class="flex-grow py-2 px-4 rounded-l-md focus:outline-none focus:ring-2 transition-all duration-500 ease-in-out pr-10"
          :class="isEnhancedMode ? 'bg-indigo-800/50 text-fuchsia-100 placeholder-fuchsia-300 focus:ring-fuchsia-500 backdrop-blur-sm' : 'bg-slate-700 text-slate-100 focus:ring-emerald-500'"
        />
        <button
          @click="sendMessage"
          class="absolute right-0 top-0 bottom-0 px-3 flex items-center justify-center transition duration-200 ease-in-out rounded-r-md"
          :class="isEnhancedMode ? 'bg-fuchsia-600 hover:bg-fuchsia-700 text-white' : 'bg-emerald-600 hover:bg-emerald-700 text-white'"
        >
          <Send :size="18" />
        </button>
      </div>
    </footer>

    <!-- 设置页面 -->
    <Transition name="fade">
      <div v-if="showSettings" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white flex items-center justify-between">
            知识库设置
            <button @click="closeSettings" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              <X :size="24" />
            </button>
          </h2>

          <!-- 添加全局设置部分 -->
          <div class="mb-6 border-b border-gray-200 dark:border-gray-700 pb-4">
            <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">全局设置</h3>
            <div class="flex items-center justify-between">
              <span class="text-gray-700 dark:text-gray-300">显示引用标签</span>
              <button
                @click="toggleReferenceDisplay"
                class="relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-200 ease-in-out"
                :class="showReferences ? 'bg-emerald-600' : 'bg-gray-400'"
                role="switch"
                :aria-checked="showReferences"
              >
                <span
                  class="inline-block w-4 h-4 transform rounded-full bg-white transition-transform duration-200 ease-in-out"
                  :class="showReferences ? 'translate-x-6' : 'translate-x-1'"
                />
              </button>
            </div>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              开启后将显示知识库的引用来源和相关度
            </p>
          </div>

          <!-- 知识库列表设置 -->
          <div class="space-y-4">
            <div v-for="(kb, index) in knowledgeBases" :key="index" class="border-b border-gray-200 dark:border-gray-700 pb-4">
              <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">知识库 {{ index + 1 }}</h3>
                <button @click="removeKnowledgeBase(index)" class="text-red-500 hover:text-red-700">
                  <Trash2 :size="18" />
                </button>
              </div>
              <div class="space-y-2">
                <input 
                  v-model="kb.name" 
                  placeholder="知识库名称" 
                  class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @input="updateKnowledgeBase(index, 'name', $event.target.value)"
                >
                <textarea 
                  v-model="kb.description" 
                  placeholder="知识库描述" 
                  class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @input="updateKnowledgeBase(index, 'description', $event.target.value)"
                ></textarea>
                <input 
                  v-model="kb.space_name" 
                  placeholder="知识库标识" 
                  class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @input="updateKnowledgeBase(index, 'space_name', $event.target.value)"
                >
                <input 
                  v-model="kb.api_url" 
                  placeholder="API地址" 
                  class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @input="updateKnowledgeBase(index, 'api_url', $event.target.value)"
                >
                <input 
                  v-model="kb.model" 
                  placeholder="模型名称" 
                  class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @input="updateKnowledgeBase(index, 'model', $event.target.value)"
                >
                <button 
                  @click="testConnection(kb)"
                  class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  :disabled="isTestingConnection"
                >
                  {{ isTestingConnection ? '测试中...' : '测试连接' }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- 保存按钮 -->
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="closeSettings" 
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
            >
              取消
            </button>
            <button 
              @click="saveSettings" 
              class="px-4 py-2 bg-emerald-500 text-white rounded-md hover:bg-emerald-600"
            >
              保存设置
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="fade">
      <div v-if="showWelcomeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full">
          <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">欢迎使用员工服务知识库</h2>
          <p class="text-gray-600 dark:text-gray-300 mb-4">
            本系统由GAMECO科创团队基于AI技术实现，目的是实现一种智能问答知识库，目前我们正在测试HR员工服务问答功能。您的使用和反馈将帮助我们进一步优化这个项目。如果你认为答案不准确，请在对话中点击反馈按钮，或者随时联系我们，感谢您的参与和使用！
          </p>
          <button 
            @click="closeWelcomeModal" 
            class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition duration-200"
          >
            我已了解，开始使用
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, computed, onUnmounted } from 'vue'
import { Send, Square, Eraser, BookOpen, X, Home, Bot, Cpu, Book, User, Settings, Trash2, ThumbsUp, ThumbsDown, Brain, Zap, Database } from 'lucide-vue-next'
import { KnowledgeBaseService } from '@/services/knowledgeBase'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'

// 配置 marked
marked.setOptions({
  gfm: true,          // GitHub Flavored Markdown
  breaks: true,       // 将换行符转换为 <br>
  tables: true,       // 启用表格支持
  pedantic: false,    // 不那么严格的解析
  sanitize: false,    // 不要净化 HTML 标签
  smartLists: true,   // 使用更智能的列表行为
  smartypants: false, // 不使用更智能的标点符号
  headerIds: false,   // 不生成标题 ID
  mangle: false,      // 不转义内联 HTML
  highlight: function(code, lang) {
    try {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    } catch (e) {
      console.error('Highlight error:', e)
      return code
    }
  }
})

const userInput = ref('')
const error = ref(null)
/** @type {import('@/types/knowledge').ChatMessage[]} */
const chatHistory = ref([
  { sender: 'ai', content: '欢迎使用GAMECO HR员工服务知识库。请输入选择对应服务模块后，输入您要了解的问题？', feedback: null }
])
const showCategories = ref(true)
const showWelcomeModal = ref(true)
const showSettings = ref(false)
const copiedIndex = ref(null)
const mainContent = ref(null)
const shouldAutoScroll = ref(true)

const categories = computed(() => {
  return knowledgeBases.value.map(kb => ({
    name: kb.name || '未命名知识库',
    icon: Book, // 默认使用 Book 图标
    description: kb.description || '暂无描述',
    space_name: kb.space_name,
    api_url: kb.api_url,
    model: kb.model
  }))
})

// 移除 isEnhancedMode，添加生成状态控制
const isGenerating = ref(false)
let currentGeneration = null // 用于存储当前生成的请求

// 停止生成方法
const stopGeneration = () => {
  if (currentGeneration) {
    currentGeneration.abort() // 中断当前请求
    currentGeneration = null
    isGenerating.value = false
    
    // 添加系统消息提示用户生成已停止
    chatHistory.value.push({
      sender: 'ai',
      content: '内容生成已停止。',
      feedback: null
    })
  }
}

// 修改发送消息方法
const sendMessage = async () => {
  if (!currentKnowledgeBase.value) {
    alert('请先选择知识库')
    return
  }
  
  if (userInput.value.trim() === '') return
  
  // 如果正在生成，则不允许发送新消息
  if (isGenerating.value) return
  
  const message = userInput.value
  chatHistory.value.push({ 
    sender: 'user', 
    content: message, 
    feedback: null 
  })
  userInput.value = ''
  scrollToBottom()
  
  try {
    isGenerating.value = true
    
    // 创建 AbortController
    const controller = new AbortController()
    currentGeneration = controller
    
    // 添加一个空的 AI 消息占位
    chatHistory.value.push({
      sender: 'ai',
      content: '',
      feedback: null,
      references: []
    })
    
    const stream = await KnowledgeBaseService.query(
      currentKnowledgeBase.value,
      message,
      controller.signal
    )
    
    let currentContent = ''
    let currentReferences = []
    
    for await (const chunk of stream) {
      if (chunk.type === 'content') {
        currentContent += chunk.text
        // 更新最后一条消息的内容
        chatHistory.value[chatHistory.value.length - 1].content = currentContent
      } else if (chunk.type === 'reference') {
        currentReferences.push({
          content: chunk.text,
          source: chunk.source,
          recall_score: chunk.similarity,
          id: chunk.id
        })
        // 更新最后一条消息的引用
        chatHistory.value[chatHistory.value.length - 1].references = currentReferences
      }
      scrollToBottom()
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Generation aborted')
    } else {
      console.error('Knowledge base query failed:', error)
      chatHistory.value.push({
        sender: 'ai',
        content: '抱歉，服务器出现错误，请稍后再试。',
        feedback: null
      })
    }
  } finally {
    isGenerating.value = false
    currentGeneration = null
  }
}

const clearChat = () => {
  chatHistory.value = [{ sender: 'ai', content: '对话清除。有什么我可以帮助您的吗？', feedback: null }]
  scrollToBottom()
}

const toggleCategories = () => {
  showCategories.value = !showCategories.value
}

// 添加当前选中卡片的状态
const selectedCardIndex = ref(null)

// 修改选择知识库的方法
const selectCategory = (category, index) => {
  currentKnowledgeBase.value = category
  selectedCardIndex.value = index // 记录选中的卡片索引
  
  // 可选：添加选择提示
  chatHistory.value.push({
    sender: 'ai',
    content: `已选择知识库: ${category.name}，您可以开始提问了。`,
    feedback: null
  })
}

const closeWelcomeModal = () => {
  showWelcomeModal.value = false
}

const copyToClipboard = (text, index) => {
  navigator.clipboard.writeText(text).then(() => {
    copiedIndex.value = index
    setTimeout(() => {
      copiedIndex.value = null
    }, 2000)
  }).catch(err => {
    console.error('无法复制文本: ', err)
  })
}

const scrollToBottom = () => {
  if (shouldAutoScroll.value) {
    nextTick(() => {
      if (mainContent.value) {
        mainContent.value.scrollTop = mainContent.value.scrollHeight
      }
    })
  }
}

const handleScroll = () => {
  if (mainContent.value) {
    const { scrollTop, scrollHeight, clientHeight } = mainContent.value
    shouldAutoScroll.value = scrollTop + clientHeight >= scrollHeight - 10
  }
}

const openSettings = () => {
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const addCategory = () => {
  categories.value.push({
    name: '新知识库',
    icon: Book,
    description: '请添加描述',
    url: ''
  })
}

const removeCategory = (index) => {
  categories.value.splice(index, 1)
}

const saveSettings = () => {
  // 保存引用显示设置
  localStorage.setItem('showReferences', showReferences.value.toString())
  
  // 保存知识库设置
  localStorage.setItem('knowledgeBases', JSON.stringify(knowledgeBases.value))
  
  // 强制重新渲染聊天记录以应用新设置
  chatHistory.value = [...chatHistory.value]
  
  closeSettings()
}

const provideFeedback = (index, type) => {
  if (chatHistory.value[index].sender === 'ai') {
    chatHistory.value[index].feedback = type
    // 这里可以添加将反馈发送到服务器的逻辑
    console.log(`Message ${index} received ${type} feedback`)
  }
}

watch(isGenerating, (newValue) => {
  if (newValue) {
    document.body.classList.add('generating-mode')
  } else {
    document.body.classList.remove('generating-mode')
  }
}, { immediate: true })

onMounted(() => {
  try {
    console.log('Innovative HR Knowledge Base component mounted successfully')
    scrollToBottom()
  } catch (e) {
    error.value = e.message
    console.error('Error in Innovative HR Knowledge Base component:', e)
  }
})

/** @type {import('@/types/knowledge').KnowledgeBase[]} */
const knowledgeBases = ref([
  {
    name: '智能员工福利',
    description: '利用AI分析为员工定制个性化利方案。',
    space_name: 'employee_benefits',
    api_url: 'http://10.240.2.140:5999/api/v2/chat/completions',
    model: 'moonshot_proxyllm'
  },
  {
    name: '灵活工作制度',
    description: '基于大数据的智排班和考勤管理系统。',
    space_name: 'flexible_work',
    api_url: 'http://10.240.2.140:5999/api/v2/chat/completions',
    model: 'moonshot_proxyllm'
  }
])

// 添加测试连接状态
const isTestingConnection = ref(false)

/** @type {import('@/types/knowledge').KnowledgeBase | null} */
const currentKnowledgeBase = ref(null)

// 知识库方法
const addKnowledgeBase = () => {
  knowledgeBases.value.push({
    name: '新知识库',
    description: '请添加描述',
    space_name: '',
    api_url: 'http://10.240.2.140:5999/api/v2/chat/completions',
    model: 'moonshot_proxyllm'
  })
}

const removeKnowledgeBase = (index) => {
  knowledgeBases.value.splice(index, 1)
}

const updateKnowledgeBase = (index, field, value) => {
  knowledgeBases.value[index] = {
    ...knowledgeBases.value[index],
    [field]: value
  }
}

// 测试知识库连接
const testConnection = async (kb) => {
  isTestingConnection.value = true
  try {
    const success = await KnowledgeBaseService.testConnection(kb)
    if (success) {
      alert('连接成功！')
    } else {
      throw new Error('连接测试失败')
    }
  } catch (error) {
    alert(`连接失败: ${error.message}`)
  } finally {
    isTestingConnection.value = false
  }
}

// 保存知识库设置
const saveKnowledgeBases = () => {
  localStorage.setItem('knowledgeBases', JSON.stringify(knowledgeBases.value))
}

// 加载知识库设置
const loadKnowledgeBases = () => {
  const savedKBs = localStorage.getItem('knowledgeBases')
  if (savedKBs) {
    knowledgeBases.value = JSON.parse(savedKBs)
  }
}

// 监听知识库变化自动保存
watch(knowledgeBases, () => {
  saveKnowledgeBases()
}, { deep: true })

// 在组件挂载时载知识库
onMounted(() => {
  loadKnowledgeBases()
})

// 发送知识库消息
const sendKnowledgeBaseMessage = async (message) => {
  if (!currentKnowledgeBase.value) {
    alert('请先选择知识库')
    return
  }

  try {
    const stream = await KnowledgeBaseService.query(currentKnowledgeBase.value, message)
    const reader = stream.getReader()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      if (value.choices?.[0]?.delta?.content) {
        chatHistory.value.push({
          sender: 'ai',
          content: value.choices[0].delta.content,
          feedback: null
        })
      }
    }
  } catch (error) {
    console.error('Knowledge base query failed:', error)
    chatHistory.value.push({
      sender: 'ai', 
      content: '知识库查询失败，请稍后重试',
      feedback: null
    })
  }
}

// 选择知识库
const selectKnowledgeBase = async (kb) => {
  currentKnowledgeBase.value = kb
  chatHistory.value.push({
    sender: 'ai',
    content: `已选择知识库: ${kb.name}`,
    feedback: null
  })
}

// 解析引用内容
const parseReferences = (referencesStr) => {
  try {
    if (typeof referencesStr === 'string') {
      // 从 title="References" references="[...]" 格式中提取 JSON
      const match = referencesStr.match(/references="(.*?)"/)
      if (match && match[1]) {
        // 解码 HTML 实体
        const decodedStr = match[1].replace(/&quot;/g, '"')
        const parsed = JSON.parse(decodedStr)
        return parsed[0]?.chunks || []
      }
    }
    return referencesStr || []
  } catch (e) {
    console.error('Failed to parse references:', e)
    return []
  }
}

// 格式化内容
const formatContent = (content) => {
  if (!content) return ''
  
  // 移除引用标记，但保留内容格式
  const parts = content.split('<references')
  return parts[0].trim()
}

// 获取相关度分数的样式类
const getScoreClass = (score) => {
  const percentage = score * 100
  if (percentage >= 90) return 'bg-green-500/20 text-green-300'
  if (percentage >= 70) return 'bg-blue-500/20 text-blue-300'
  return 'bg-gray-500/20 text-gray-300'
}

// 添加弹窗位置计算方法
const getPopupPosition = (event) => {
  if (!event || !event.target) return {}
  
  const target = event.target.getBoundingClientRect()
  const windowHeight = window.innerHeight
  const windowWidth = window.innerWidth
  
  // 计算弹窗位置
  let top = target.top - 10 // 默认显示在标签上方
  let left = target.left
  
  // 如果弹窗会超出屏幕顶部，则显示在标签下方
  if (top < 0) {
    top = target.bottom + 10
  }
  
  // 确保弹窗不会超出屏幕右侧
  if (left + 400 > windowWidth) { // 400px 是弹窗的最大宽度
    left = windowWidth - 420 // 留出一些边距
  }
  
  return {
    top: `${top}px`,
    left: `${left}px`
  }
}

// 弹窗相关状态
const activePopupIndex = ref(null)
const keepPopup = ref(false)
const popup = ref(null)
const popupPosition = ref({})
const arrowPosition = ref({})
const isPopupVisible = ref(false)

// 显示弹窗
const showPopup = (event, index) => {
  // 如果当前弹窗已经显示，则不重新计算位置
  if (activePopupIndex.value === index && isPopupVisible.value) {
    return
  }
  
  // 先清除之前的状态
  hidePopup()
  
  // 设置新的弹窗状态
  activePopupIndex.value = index
  isPopupVisible.value = true
  
  // 使用 nextTick 确保 DOM 更新后再计算位置
  nextTick(() => {
    calculatePopupPosition(event)
  })
}

// 分离位置计算逻辑
const calculatePopupPosition = (event) => {
  if (!popup.value) return
  
  const target = event.currentTarget.getBoundingClientRect()
  const popupRect = popup.value.getBoundingClientRect()
  const windowWidth = window.innerWidth
  const windowHeight = window.innerHeight
  const padding = 20 // 安全边距
  
  // 计算最佳位置
  let position = {
    top: 0,
    left: 0,
    transformOrigin: ''
  }
  
  // 水平位置计算
  if (target.left + popupRect.width + padding > windowWidth) {
    position.left = Math.max(padding, windowWidth - popupRect.width - padding)
    position.transformOrigin = 'right'
  } else {
    position.left = Math.max(padding, target.left)
    position.transformOrigin = 'left'
  }
  
  // 垂直位置计算
  const spaceAbove = target.top
  const spaceBelow = windowHeight - target.bottom
  
  if (spaceAbove > spaceBelow && spaceAbove >= popupRect.height + padding) {
    // 上方空间足够
    position.top = target.top - popupRect.height - 8
    position.transformOrigin += ' bottom'
    arrowPosition.value = {
      bottom: '-8px',
      left: target.left - position.left + target.width / 2 - 8,
      display: 'block'
    }
  } else if (spaceBelow >= popupRect.height + padding) {
    // 下方空间足够
    position.top = target.bottom + 8
    position.transformOrigin += ' top'
    arrowPosition.value = {
      top: '-8px',
      left: target.left - position.left + target.width / 2 - 8,
      display: 'block'
    }
  } else {
    // 上下空间都不足，居中显示
    position.top = Math.max(padding, (windowHeight - popupRect.height) / 2)
    position.transformOrigin += ' center'
    arrowPosition.value = { display: 'none' }
  }
  
  // 应用位置
  popupPosition.value = {
    top: `${position.top}px`,
    left: `${position.left}px`,
    transformOrigin: position.transformOrigin
  }
}

// 隐藏弹窗
const hidePopup = () => {
  if (!keepPopup.value) {
    activePopupIndex.value = null
    isPopupVisible.value = false
    // 重置位置和箭状态
    popupPosition.value = {}
    arrowPosition.value = {}
  }
}

// 监听全局事件
onMounted(() => {
  const handleGlobalEvents = (event) => {
    // 检查点击是否在弹窗或引用标签内
    const isPopupClick = event.target.closest('.reference-popup')
    const isReferenceClick = event.target.closest('.reference-tag')
    
    if (!isPopupClick && !isReferenceClick) {
      hidePopup()
      keepPopup.value = false
    }
  }
  
  window.addEventListener('click', handleGlobalEvents)
  window.addEventListener('scroll', hidePopup, true)
  window.addEventListener('resize', hidePopup)
  
  onUnmounted(() => {
    window.removeEventListener('click', handleGlobalEvents)
    window.removeEventListener('scroll', hidePopup, true)
    window.removeEventListener('resize', hidePopup)
  })
})

// 安全的内容渲染函数
const renderContent = (content) => {
  try {
    if (!content) return ''
    
    // 移除引用标记，但保留内容格式
    const cleanContent = content.split('<references')[0].trim()
    
    // 预处理内容
    let processedContent = cleanContent
      .replace(/\n{3,}/g, '\n\n')
      .replace(/(\n\s*[-*]\s.*?)(\n{2,})(?=\s*[-*]\s)/g, '$1\n')
      .replace(/(?<!^\n|^\s*$)(\n\s*[-*]\s)/g, '\n\n$1')
      .replace(/(\d+)\.\s+/g, '$1\\. ')
      .replace(/\\n/g, '\n')
    
    // 将内容转换为 HTML
    const rawHtml = marked(processedContent)
    
    // 净化 HTML
    return DOMPurify.sanitize(rawHtml, {
      ADD_TAGS: ['table', 'thead', 'tbody', 'tr', 'th', 'td', 'br', 'pre', 'code', 'ul', 'ol', 'li'],
      ADD_ATTR: ['class'],
      FORBID_TAGS: ['script', 'style', 'iframe'],
      FORBID_ATTR: ['onerror', 'onclick', 'onload'],
      ALLOW_DATA_ATTR: false
    })
  } catch (e) {
    console.error('Render error:', e)
    return content
  }
}

// 更新引用内容获取方法
const getReferences = (message) => {
  try {
    // 如果禁用了引用显示，直接返回空数组
    if (!showReferences.value) {
      return []
    }

    // 如果已经是解析过的引用数组，直接返回
    if (Array.isArray(message.references)) {
      return message.references
    }
    
    // 如果是字符串形式的引用，解析它
    if (typeof message.content === 'string' && message.content.includes('<references')) {
      const referencesMatch = message.content.match(/<references.*?\/>/)
      if (referencesMatch) {
        const match = referencesMatch[0].match(/references="(.*?)"/)
        if (match && match[1]) {
          const decodedStr = match[1].replace(/&quot;/g, '"')
          const parsed = JSON.parse(decodedStr)
          return parsed[0]?.chunks || []
        }
      }
    }
    
    return []
  } catch (e) {
    console.error('Failed to parse references:', e)
    return []
  }
}

// 更新引用显示控制
const showReferences = ref(localStorage.getItem('showReferences') !== 'false') // 默认为 true

// 切换引用显示状态
const toggleReferenceDisplay = () => {
  showReferences.value = !showReferences.value
  localStorage.setItem('showReferences', showReferences.value.toString())
}

// 在组件挂载时加载引用显示设置
onMounted(() => {
  // 从本地存储加载引用显示设置
  const savedShowReferences = localStorage.getItem('showReferences')
  if (savedShowReferences !== null) {
    showReferences.value = savedShowReferences === 'true'
  }
})

// 监听引用显示状态变化
watch(showReferences, (newValue) => {
  // 强制重新渲染聊天记录
  chatHistory.value = [...chatHistory.value]
})
</script>

<style>
@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

@keyframes gradient-x {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient-x {
  animation: gradient-x 3s ease infinite;
  background-size: 200% 200%;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  height: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 添加引用悬浮框的过渡效果 */
.group/ref:hover .absolute {
  opacity: 1;
  transform: translateY(0);
}

.absolute {
  transform: translateY(4px);
  transition: all 0.2s ease-in-out;
}

/* 优化引用悬浮效果 */
.group/ref {
  position: relative;
}

.group/ref:hover .absolute {
  opacity: 1;
  transform: translateY(0);
}

/* 添加阴影和模糊效果 */
.shadow-xl {
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.3);
  backdrop-filter: blur(8px);
}

/* 平滑过渡动画 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* 更新弹窗相关样式 */
.group/ref {
  position: relative;
}

/* 移除之前的 transform 相关样式 */
.group/ref:hover .fixed {
  opacity: 1;
}

/* 优化阴影和模糊效果 */
.shadow-xl {
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.3);
  backdrop-filter: blur(8px);
}

/* 添加弹窗动画 */
.fixed {
  transition: opacity 0.2s ease-in-out;
  pointer-events: auto;
}

/* 确保弹窗在最上层 */
.z-\[9999\] {
  z-index: 9999;
}

/* 自定义滚动条样式 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

/* 弹窗动画优化 */
.transition {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.duration-200 {
  transition-duration: 200ms;
}

.duration-150 {
  transition-duration: 150ms;
}

.ease-out {
  transition-timing-function: cubic-bezier(0, 0, 0.2, 1);
}

.ease-in {
  transition-timing-function: cubic-bezier(0.4, 0, 1, 1);
}

/* 优化弹窗相关样式 */
.reference-popup {
  pointer-events: auto;
  will-change: transform, opacity;
}

.reference-tag {
  position: relative;
  z-index: 1;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-10%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

/* 更新 Markdown 样式 */
.markdown-content {
  line-height: 1.6;
  font-size: 1rem;
}

/* 调整段落间距 */
.markdown-content p {
  margin: 0.75em 0;  /* 减小段落间距 */
}

/* 优化列表样式 */
.markdown-content ul,
.markdown-content ol {
  margin: 0.75em 0;  /* 减小列表与其他元素的间距 */
  padding-left: 1.5em;  /* 减小缩进 */
}

.markdown-content li {
  margin: 0.25em 0;  /* 减小列表项间距 */
  padding-left: 0.25em;  /* 微调列表项缩进 */
}

/* 有序列表样式 */
.markdown-content ol {
  list-style-type: decimal;  /* 使用数字序号 */
  counter-reset: item;  /* 重置计数器 */
}

.markdown-content ol li {
  counter-increment: item;  /* 增加计数器 */
  list-style-position: outside;  /* 序号位于内容外 */
}

/* 无序列表样式 */
.markdown-content ul {
  list-style-type: disc;  /* 实心圆点 */
}

.markdown-content ul ul {
  list-style-type: circle;  /* 二级列表使用空心圆点 */
}

/* 确保列表项内容对齐 */
.markdown-content li > * {
  margin-top: 0;
  margin-bottom: 0;
}

/* 调整列表项与段落的间距 */
.markdown-content li p {
  margin: 0.25em 0;  /* 减小列表项内段落的间距 */
}

/* 添加开关按钮动画 */
.translate-x-1 {
  transform: translateX(0.25rem);
}

.translate-x-6 {
  transform: translateX(1.5rem);
}

.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* 添加卡片选中效果的过渡动画 */
.ring-2 {
  transition: all 0.3s ease-in-out;
}

/* 添加阴影过渡效果 */
.shadow-lg {
  transition: box-shadow 0.3s ease-in-out;
}

/* 优化 hover 缩放效果 */
.transform {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.hover\:scale-105:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
</style>