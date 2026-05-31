import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Scoreboard from '../../src/components/Scoreboard.vue'

describe('Scoreboard', () => {
  const players = [
    { name: 'Alice', num_cards: 3 },
    { name: 'Bob', num_cards: 5 },
    { name: 'Charlie', num_cards: 4 },
  ]

  it('renders all players', () => {
    const wrapper = mount(Scoreboard, {
      props: {
        players,
        currentGuesser: 'Alice',
        myName: 'Alice',
      },
    })
    expect(wrapper.text()).toContain('Alice')
    expect(wrapper.text()).toContain('Bob')
    expect(wrapper.text()).toContain('Charlie')
  })

  it('shows card counts', () => {
    const wrapper = mount(Scoreboard, {
      props: {
        players,
        currentGuesser: 'Alice',
        myName: 'Alice',
      },
    })
    expect(wrapper.text()).toContain('3')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('4')
  })

  it('highlights current guesser', () => {
    const wrapper = mount(Scoreboard, {
      props: {
        players,
        currentGuesser: 'Bob',
        myName: 'Alice',
      },
    })
    const items = wrapper.findAll('.scoreboard-item')
    expect(items[1].classes()).toContain('active')
    expect(items[0].classes()).not.toContain('active')
  })

  it('marks current player with You badge', () => {
    const wrapper = mount(Scoreboard, {
      props: {
        players,
        currentGuesser: 'Alice',
        myName: 'Alice',
      },
    })
    expect(wrapper.text()).toContain('You')
  })

  it('marks current player with is-me class', () => {
    const wrapper = mount(Scoreboard, {
      props: {
        players,
        currentGuesser: 'Bob',
        myName: 'Alice',
      },
    })
    const items = wrapper.findAll('.scoreboard-item')
    expect(items[0].classes()).toContain('is-me')
  })
})
