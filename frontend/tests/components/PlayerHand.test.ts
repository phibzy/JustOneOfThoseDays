import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PlayerHand from '../../src/components/PlayerHand.vue'

describe('PlayerHand', () => {
  it('shows empty message when no cards', () => {
    const wrapper = mount(PlayerHand, {
      props: {
        cards: [],
      },
    })
    expect(wrapper.text()).toContain('No cards yet')
  })

  it('renders card list', () => {
    const wrapper = mount(PlayerHand, {
      props: {
        cards: [
          { desc: 'Stub toe', value: 5 },
          { desc: 'Flat tire', value: 24.5 },
        ],
      },
    })
    expect(wrapper.text()).toContain('Stub toe')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('Flat tire')
    expect(wrapper.text()).toContain('24.5')
  })

  it('uses custom title', () => {
    const wrapper = mount(PlayerHand, {
      props: {
        cards: [],
        title: 'My Cards',
      },
    })
    expect(wrapper.text()).toContain('My Cards')
  })

  it('defaults to "Your Hand" title', () => {
    const wrapper = mount(PlayerHand, {
      props: {
        cards: [],
      },
    })
    expect(wrapper.text()).toContain('Your Hand')
  })
})
