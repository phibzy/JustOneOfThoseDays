<script setup lang="ts">
import { ref, watch, onUnmounted, computed } from 'vue'

const props = defineProps<{
  active: boolean
  duration: number
}>()

const emit = defineEmits<{
  (e: 'timeout'): void
}>()

const timeLeft = ref(props.duration)
let intervalId: ReturnType<typeof setInterval> | null = null

const timerClass = computed(() => {
  if (timeLeft.value <= 5) return 'danger'
  if (timeLeft.value <= 10) return 'warning'
  return 'normal'
})

function startTimer() {
  stopTimer()
  timeLeft.value = props.duration
  intervalId = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      stopTimer()
      emit('timeout')
    }
  }, 1000)
}

function stopTimer() {
  if (intervalId !== null) {
    clearInterval(intervalId)
    intervalId = null
  }
}

watch(
  () => props.active,
  (newVal) => {
    if (newVal) {
      startTimer()
    } else {
      stopTimer()
    }
  },
  { immediate: true }
)

onUnmounted(() => {
  stopTimer()
})
</script>

<template>
  <div v-if="active" class="timer" :class="timerClass">
    ⏱ {{ timeLeft }}s
  </div>
</template>
