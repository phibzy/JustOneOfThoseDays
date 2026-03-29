<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/game'

const router = useRouter()
const store = useGameStore()

const playerNames = ref<string[]>(['', ''])
const shareLinks = ref<Record<string, string> | null>(null)
const creating = ref(false)
const errorMsg = ref('')

const canStart = computed(() => {
  const filled = playerNames.value.filter((n) => n.trim().length > 0)
  return filled.length >= 2
})

function addPlayer() {
  if (playerNames.value.length < 8) {
    playerNames.value.push('')
  }
}

function removePlayer(index: number) {
  if (playerNames.value.length > 2) {
    playerNames.value.splice(index, 1)
  }
}

async function startGame() {
  const names = playerNames.value
    .map((n) => n.trim())
    .filter((n) => n.length > 0)

  if (names.length < 2) {
    errorMsg.value = 'Need at least 2 players'
    return
  }

  creating.value = true
  errorMsg.value = ''

  try {
    const data = await store.createGame(names)

    // Build share links for each player
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
        v-for="(_, index) in playerNames"
        :key="index"
        class="player-input-row"
      >
        <div class="player-number">{{ index + 1 }}</div>
        <input
          v-model="playerNames[index]"
          class="input"
          :placeholder="`Player ${index + 1} name`"
          @keyup.enter="startGame"
        />
        <button
          v-if="playerNames.length > 2"
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
          @click="addPlayer"
          :disabled="playerNames.length >= 8"
        >
          + Add Player
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
        Share these links with each player to join the game.
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
