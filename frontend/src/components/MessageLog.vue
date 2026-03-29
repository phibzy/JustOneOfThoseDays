<script setup lang="ts">
defineProps<{
  messages: string[]
}>()
</script>

<template>
  <div class="panel">
    <div class="panel-header">
      <h3>Activity</h3>
    </div>
    <ul class="message-log">
      <li v-for="(msg, i) in messages" :key="i">{{ msg }}</li>
    </ul>
    <div
      v-if="messages.length === 0"
      style="color: var(--text-muted); text-align: center; padding: 16px;"
    >
      No activity yet
    </div>
  </div>
</template>
