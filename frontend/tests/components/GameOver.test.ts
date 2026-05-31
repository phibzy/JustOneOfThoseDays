import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import GameOver from '../../src/components/GameOver.vue'

describe('GameOver', () => {
  const players = [
    { name: 'Alice', num_cards: 10 },
    { name: 'Bob', num_cards: 7 },
  ]

  it('shows winner name', () => {
    const wrapper = mount(GameOver, {
      props: {
        winner: 'Alice',
        players,
      },
    })
    expect(wrapper.text()).toContain('Alice Wins!')
    expect(wrapper.text()).toContain('Congratulations!')
  })

  it('shows no winner message when winner is null', () => {
    const wrapper = mount(GameOver, {
      props: {
        winner: null,
        players,
      },
    })
    expect(wrapper.text()).toContain('No Winner')
    expect(wrapper.text()).toContain('Nobody managed to win')
  })

  it('shows final scores', () => {
    const wrapper = mount(GameOver, {
      props: {
        winner: 'Alice',
        players,
      },
    })
    expect(wrapper.text()).toContain('10')
    expect(wrapper.text()).toContain('7')
  })

  it('emits play-again on button click', async () => {
    const wrapper = mount(GameOver, {
      props: {
        winner: 'Alice',
        players,
      },
    })
    await wrapper.find('.btn-primary').trigger('click')
    expect(wrapper.emitted('play-again')).toBeTruthy()
  })

  it('highlights winner in scoreboard', () => {
    const wrapper = mount(GameOver, {
      props: {
        winner: 'Alice',
        players,
      },
    })
    const items = wrapper.findAll('.scoreboard-item')
    expect(items[0].classes()).toContain('active')
    expect(items[1].classes()).not.toContain('active')
  })
})
