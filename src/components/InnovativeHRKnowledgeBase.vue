<template>
    <div
      class="flex flex-col h-screen transition-all duration-1000 ease-in-out"
      :class="isEnhancedMode ? 'bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800' : 'bg-gradient-to-br from-slate-900 to-slate-800'"
    >
      <header
        class="flex justify-between items-center p-4"
        :class="isEnhancedMode ? 'bg-indigo-900/50 backdrop-blur-md' : 'bg-slate-800'"
      >
        <h1
          class="text-2xl font-bold flex items-center"
          :class="isEnhancedMode ? 'text-fuchsia-400 animate-pulse' : 'text-emerald-400'"
        >
          <Cpu class="mr-2" :size="24" />
          智能HR知识库
          <span v-if="isEnhancedMode" class="text-sm ml-2 bg-fuchsia-700 px-2 py-1 rounded-full">AI增强</span>
        </h1>
        <div class="flex gap-4">
          <button 
            @click="openSettings" 
            class="text-slate-400 hover:text-fuchsia-400 transition-colors" 
            aria-label="设置"
          >
            <Settings :size="24" />
          </button>
          <button class="text-slate-400 hover:text-fuchsia-400 transition-colors" aria-label="返回主页">
            <Home :size="24" />
          </button>
          <button class="text-slate-400 hover:text-slate-100 transition-colors" aria-label="关闭">
            <X :size="24" />
          </button>
        </div>
      </header>
  
      <main ref="mainContent" class="flex-grow overflow-y-auto p-6 space-y-4" @scroll="handleScroll">
        <div class="flex justify-around mb-6" :class="isEnhancedMode ? 'text-fuchsia-300' : 'text-emerald-300'">
          <div class="flex flex-col items-center">
            <Brain class="w-8 h-8 mb-2 animate-pulse" />
            <span>AI分析</span>
          </div>
          <div class="flex flex-col items-center">
            <Zap class="w-8 h-8 mb-2 animate-bounce" />
            <span>实时更新</span>
          </div>
          <div class="flex flex-col items-center">
            <Database class="w-8 h-8 mb-2 animate-spin-slow" />
            <span>智能匹配</span>
          </div>
        </div>
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong class="font-bold">Error:</strong>
          <span class="block sm:inline">{{ error }}</span>
        </div>
        
        <div v-if="showCategories" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          <div v-for="category in categories" :key="category.name" 
               class="bg-slate-800 rounded-lg p-4 hover:bg-slate-700 transition-all duration-300 cursor-pointer transform hover:scale-105"
               :class="isEnhancedMode ? 'border border-fuchsia-500/30 hover:border-fuchsia-500' : ''"
               @click="selectCategory(category.name)">
            <h3 class="text-lg font-semibold mb-2 flex items-center" :class="isEnhancedMode ? 'text-fuchsia-400' : 'text-emerald-400'">
              <component :is="category.icon" class="mr-2" :size="18" />
              {{ category.name }}
            </h3>
            <p :class="isEnhancedMode ? 'text-fuchsia-200' : 'text-slate-300'">{{ category.description }}</p>
          </div>
        </div>
  
        <div class="space-y-4">
          <div v-for="(message, index) in chatHistory" :key="index" class="flex items-start space-x-2 group">
            <Bot v-if="message.sender === 'ai'" :class="isEnhancedMode ? 'text-fuchsia-400' : 'text-emerald-400'" class="w-8 h-8 mt-1" />
            <User v-else :class="isEnhancedMode ? 'text-fuchsia-400' : 'text-emerald-400'" class="w-8 h-8 mt-1" />
            <div
              v-if="message.sender === 'ai'"
              class="rounded-lg p-4 shadow-lg max-w-3xl relative overflow-hidden group"
              :class="isEnhancedMode 
                ? 'bg-indigo-800/50 backdrop-blur-sm border border-fuchsia-500/50 shadow-fuchsia-500/20' 
                : 'bg-slate-700'"
            >
              <p :class="isEnhancedMode ? 'text-fuchsia-100' : 'text-slate-300'">
                {{ message.content }}
              </p>
              <div v-if="isEnhancedMode" class="absolute -bottom-4 -right-4 w-24 h-24 bg-fuchsia-500 rounded-full opacity-20 animate-ping"></div>
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
            <div
              v-else
              class="rounded-lg p-4 shadow-lg max-w-3xl relative overflow-hidden"
              :class="[
                message.sender === 'user' 
                  ? isEnhancedMode 
                    ? 'bg-fuchsia-800/50 backdrop-blur-sm border border-indigo-500/50 shadow-indigo-500/20' 
                    : 'bg-slate-600'
                  : isEnhancedMode
                    ? 'bg-indigo-800/50 backdrop-blur-sm border border-fuchsia-500/50 shadow-fuchsia-500/20' 
                    : 'bg-slate-700'
              ]"
            >
              <p :class="isEnhancedMode ? 'text-fuchsia-100' : 'text-slate-300'">
                {{ message.content }}
              </p>
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
  
      <footer
        class="p-4"
        :class="isEnhancedMode ? 'bg-indigo-900/50 backdrop-blur-md' : 'bg-slate-800'"
      >
        <div class="flex gap-2 mb-2">
          <button
            @click="toggleEnhancedMode"
            class="flex-1 py-2 px-4 rounded-md transition duration-500 ease-in-out relative overflow-hidden"
            :class="isEnhancedMode ? 'bg-fuchsia-600 hover:bg-fuchsia-700 text-white shadow-lg shadow-fuchsia-500/50' : 'bg-emerald-600 hover:bg-emerald-700 text-white'"
          >
            <span class="relative z-10 flex items-center justify-center">
              <Zap :size="18" class="mr-2" />
              {{ isEnhancedMode ? '关闭AI增强' : '开启AI增强' }}
            </span>
            <div v-if="isEnhancedMode" class="absolute inset-0 bg-gradient-to-r from-fuchsia-500 to-pink-500 animate-gradient-x"></div>
          </button>
          <button
            @click="clearChat"
            class="flex-1 py-2 px-4 rounded-md transition duration-200 ease-in-out"
            :class="isEnhancedMode ? 'bg-indigo-600 hover:bg-indigo-700 text-fuchsia-100' : 'bg-slate-600 hover:bg-slate-700 text-white'"
          >
            <Eraser :size="18" class="inline mr-2" />
            清除对话
          </button>
          <button
            @click="toggleCategories"
            class="flex-1 py-2 px-4 rounded-md transition duration-200 ease-in-out"
            :class="isEnhancedMode ? 'bg-indigo-600 hover:bg-indigo-700 text-fuchsia-100' : 'bg-slate-600 hover:bg-slate-700 text-white'"
          >
            <BookOpen :size="18" class="inline mr-2" />
            {{ showCategories ? '隐藏目录' : '显示目录' }}
          </button>
        </div>
        <div class="flex relative">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="输入您的HR相关问题..."
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
            <div class="space-y-4">
              <div v-for="(category, index) in categories" :key="index" class="border-b border-gray-200 dark:border-gray-700 pb-4">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300">{{ category.name }}</h3>
                  <button @click="removeCategory(index)" class="text-red-500 hover:text-red-700">
                    <Trash2 :size="18" />
                  </button>
                </div>
                <div class="space-y-2">
                  <input v-model="category.name" placeholder="知识库名称" class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                  <input v-model="category.description" placeholder="简介" class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                  <input v-model="category.url" placeholder="知识库地址" class="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                </div>
              </div>
            </div>
            <button @click="addCategory" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              添加新知识库
            </button>
            <button @click="saveSettings" class="mt-4 ml-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
              保存设置
            </button>
          </div>
        </div>
      </Transition>
  
      <Transition name="fade">
        <div v-if="showWelcomeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl max-w-md w-full">
            <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">欢迎使用智能HR知识库</h2>
            <p class="text-gray-600 dark:text-gray-300 mb-4">
              本系统基于科创项目实现，答案可能存在不准确。您的使用和反馈将提供给我们的团队进行进一步优化。感谢您的参与和使用！
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
  import { ref, watch, onMounted, nextTick } from 'vue'
  import { Send, Zap, Eraser, BookOpen, X, Home, Bot, Brain, Database, Cpu, Users, Calendar, TrendingUp, Briefcase, UserPlus, Book, User, Settings, Trash2, ThumbsUp, ThumbsDown } from 'lucide-vue-next'
  
  const isEnhancedMode = ref(false)
  const userInput = ref('')
  const error = ref(null)
  const chatHistory = ref([
    { sender: 'ai', content: '欢迎使用智能HR知识库。我能为您提供哪些HR相关的信息或服务？', feedback: null }
  ])
  const showCategories = ref(true)
  const showWelcomeModal = ref(true)
  const showSettings = ref(false)
  const copiedIndex = ref(null)
  const mainContent = ref(null)
  const shouldAutoScroll = ref(true)
  
  const categories = ref([
    { name: '智能员工福利', icon: Users, description: '利用AI分析为员工定制个性化福利方案。', url: '' },
    { name: '灵活工作制度', icon: Calendar, description: '基于大数据的智能排班和考勤管理系统。', url: '' },
    { name: '数据驱动绩效', icon: TrendingUp, description: '使用机器学习算法进行全方位绩效评估。', url: '' },
    { name: '智能学习平台', icon: Brain, description: 'AI推荐的个性化培训课程和职业发展路径。', url: '' },
    { name: '数字化入职', icon: UserPlus, description: 'VR/AR技术辅助的沉浸式入职体验。', url: '' },
    { name: '智能政策管理', icon: Book, description: '自动更新的公司制度库，支持自然语言查询。', url: '' },
  ])
  
  const toggleEnhancedMode = () => {
    isEnhancedMode.value = !isEnhancedMode.value
    if (isEnhancedMode.value) {
      chatHistory.value.push({ sender: 'ai', content: '智能模式已激活。我可以为您提供AI驱动的HR解决方案，包括实时政策更新、个性化工作流程建议和预测性分析。请问有什么我可以协助您的？', feedback: null })
      scrollToBottom()
    }
  }
  
  const sendMessage = () => {
    if (userInput.value.trim() === '') return
    
    chatHistory.value.push({ sender: 'user', content: userInput.value, feedback: null })
    scrollToBottom()
    
    // 模拟AI响应
    setTimeout(() => {
      const aiResponse = `感谢您的问题。关于"${userInput.value}"，我们的AI系统正在分析最新的HR数据和政策。请稍等，我们将为您提供最准确和个性化的答复。`
      chatHistory.value.push({ sender: 'ai', content: aiResponse, feedback: null })
      scrollToBottom()
    }, 1000)
    
    userInput.value = ''
  }
  
  const clearChat = () => {
    chatHistory.value = [{ sender: 'ai', content: '对话已清除。有什么我可以帮助您的吗？', feedback: null }]
    scrollToBottom()
  }
  
  const toggleCategories = () => {
    showCategories.value = !showCategories.value
  }
  
  const selectCategory = (categoryName) => {
    chatHistory.value = [{ sender: 'ai', content: `欢迎了解${categoryName}。我可以为您提供相关的详细信息和解答问题。请问您想了解哪些具体方面？`, feedback: null }]
    userInput.value = ''
    scrollToBottom()
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
    // 这里可以添加保存设置的逻辑，比如发送到服务器
    console.log('保存设置:', categories.value)
    closeSettings()
  }
  
  const provideFeedback = (index, type) => {
    if (chatHistory.value[index].sender === 'ai') {
      chatHistory.value[index].feedback = type
      // 这里可以添加将反馈发送到服务器的逻辑
      console.log(`Message ${index} received ${type} feedback`)
    }
  }
  
  watch(isEnhancedMode, (newValue) => {
    if (newValue) {
      document.body.classList.add('enhanced-mode')
    } else {
      document.body.classList.remove('enhanced-mode')
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
  </style>