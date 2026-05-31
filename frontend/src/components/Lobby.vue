<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/game'
import type { PlayerSlot } from '../types/game'

const router = useRouter()
const store = useGameStore()

const players = ref<PlayerSlot[]>([
  { name: '', is_cpu: false },
  { name: '', is_cpu: false },
])
const shareLinks = ref<Record<string, string> | null>(null)
const creating = ref(false)
const errorMsg = ref('')

const canStart = computed(() => players.value.length >= 2)

function addPlayer(isCpu: boolean) {
  if (players.value.length < 8) {
    players.value.push({ name: '', is_cpu: isCpu })
  }
}

function removePlayer(index: number) {
  if (players.value.length > 2) {
    players.value.splice(index, 1)
  }
}

function toggleCpu(index: number) {
  players.value[index].is_cpu = !players.value[index].is_cpu
}

function defaultName(slot: PlayerSlot, index: number): string {
  const trimmed = slot.name.trim()
  if (trimmed.length > 0) return trimmed
  return slot.is_cpu ? `CPU ${index + 1}` : `Player ${index + 1}`
}

async function startGame() {
  const slots: PlayerSlot[] = players.value.map((p, i) => ({
    name: defaultName(p, i),
    is_cpu: p.is_cpu,
  }))

  const humanCount = slots.filter((s) => !s.is_cpu).length
  if (slots.length < 2) {
    errorMsg.value = 'Need at least 2 players'
    return
  }
  if (humanCount < 1) {
    errorMsg.value = 'Need at least 1 human player'
    return
  }

  creating.value = true
  errorMsg.value = ''

  try {
    const data = await store.createGame(slots)

    // Build share links only for human players (CPUs never connect).
    const baseUrl = window.location.origin
    const links: Record<string, string> = {}
    for (const [name, token] of Object.entries(data.player_tokens)) {
      links[name] = `${baseUrl}/game/${data.game_id}?player=${encodeURIComponent(name)}&token=${encodeURIComponent(token)}`
    }
    shareLinks.value = links
  } catch (e) {
    errorMsg.value = (e as Error).message
  } finally {
    creating.value = false
  }
}

function openPlayerLink(name: string, _link: string) {
  const token = store.allTokens[name]
  store.setPlayer(name, token)
  router.push(`/game/${store.gameId}?player=${encodeURIComponent(name)}&token=${encodeURIComponent(token)}`)
}
</script>

<template>
  <div class="lobby-container">
    <div class="lobby-panel panel" v-if="!shareLinks">
      <h1 class="lobby-title">Just One Of Those Days</h1>
      <p class="lobby-subtitle">A card game of miserable experiences. How bad can it get?</p>

      <div
        v-for="(player, index) in players"
        :key="index"
        class="player-input-row"
      >
        <div class="player-number">{{ index + 1 }}</div>
        <input
          v-model="players[index].name"
          class="input"
          :placeholder="player.is_cpu ? `CPU ${index + 1}` : `Player ${index + 1} name`"
          @keyup.enter="startGame"
        />
        <button
          class="btn btn-outline btn-sm"
          :class="{ 'btn-primary': player.is_cpu }"
          @click="toggleCpu(index)"
          :aria-pressed="player.is_cpu"
          title="Toggle CPU player"
        >
          {{ player.is_cpu ? '🤖 CPU' : '🧑 Human' }}
        </button>
        <button
          v-if="players.length > 2"
          class="btn btn-outline btn-sm"
          @click="removePlayer(index)"
          aria-label="Remove player"
        >
          ✕
        </button>
      </div>

      <div class="lobby-actions">
        <button
          class="btn btn-outline"
          @click="addPlayer(false)"
          :disabled="players.length >= 8"
        >
          + Add Player
        </button>
        <button
          class="btn btn-outline"
          @click="addPlayer(true)"
          :disabled="players.length >= 8"
        >
          + Add CPU
        </button>
        <button
          class="btn btn-primary btn-lg"
          @click="startGame"
          :disabled="!canStart || creating"
        >
          {{ creating ? 'Creating...' : 'Start Game' }}
        </button>
      </div>

      <p v-if="errorMsg" style="color: var(--danger); margin-top: 12px; text-align: center;">
        {{ errorMsg }}
      </p>
    </div>

    <!-- Share links panel -->
    <div v-else class="lobby-panel panel share-panel">
      <h2 style="text-align: center; margin-bottom: 8px;">Game Created! 🎉</h2>
      <p class="lobby-subtitle">
        Share these links with each human player to join the game.
        CPU players take their turns automatically.
      </p>

      <div
        v-for="(link, name) in shareLinks"
        :key="name"
        class="share-link"
      >
        <span class="share-name">{{ name }}</span>
        <span class="share-url">{{ link }}</span>
        <button class="btn btn-primary btn-sm" @click="openPlayerLink(String(name), link)">
          Play
        </button>
      </div>

      <div class="lobby-actions" style="margin-top: 24px;">
        <button class="btn btn-outline" @click="shareLinks = null">
          ← Back
        </button>
      </div>
    </div>
  </div>
</template>
