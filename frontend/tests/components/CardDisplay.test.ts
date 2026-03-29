import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import CardDisplay from '../../src/components/CardDisplay.vue'

describe('CardDisplay', () => {
  it('renders card description', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Stub toe on chair leg' },
      },
    })
    expect(wrapper.text()).toContain('Stub toe on chair leg')
  })

  it('hides value by default', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Test', value: 42 },
      },
    })
    expect(wrapper.text()).toContain('???')
    expect(wrapper.text()).not.toContain('42')
  })

  it('shows value when showValue is true', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Test', value: 42 },
        showValue: true,
      },
    })
    expect(wrapper.text()).toContain('42')
  })

  it('shows ??? when value is not present', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Test' },
        showValue: true,
      },
    })
    expect(wrapper.text()).toContain('???')
  })

  it('renders with large size class', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Test' },
        size: 'large',
      },
    })
    expect(wrapper.find('.game-card-large').exists()).toBe(true)
  })

  it('renders Misery Card label', () => {
    const wrapper = mount(CardDisplay, {
      props: {
        card: { desc: 'Test card' },
      },
    })
    expect(wrapper.text()).toContain('Misery Card')
  })
})
