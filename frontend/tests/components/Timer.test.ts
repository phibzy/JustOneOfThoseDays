import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Timer from '../../src/components/Timer.vue'

describe('Timer', () => {
  it('renders when active', () => {
    const wrapper = mount(Timer, {
      props: {
        active: true,
        duration: 30,
      },
    })
    expect(wrapper.find('.timer').exists()).toBe(true)
    expect(wrapper.text()).toContain('30s')
  })

  it('does not render when inactive', () => {
    const wrapper = mount(Timer, {
      props: {
        active: false,
        duration: 30,
      },
    })
    expect(wrapper.find('.timer').exists()).toBe(false)
  })

  it('has normal class when time is plenty', () => {
    const wrapper = mount(Timer, {
      props: {
        active: true,
        duration: 30,
      },
    })
    expect(wrapper.find('.timer').classes()).toContain('normal')
  })
})
