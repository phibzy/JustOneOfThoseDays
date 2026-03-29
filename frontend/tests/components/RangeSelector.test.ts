import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RangeSelector from '../../src/components/RangeSelector.vue'

describe('RangeSelector', () => {
  const defaultRanges = [
    { index: 1, low: 0, high: 30 },
    { index: 2, low: 30, high: 60 },
    { index: 3, low: 60, high: 100 },
  ]

  it('renders all range options', () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [],
        disabled: false,
      },
    })
    const buttons = wrapper.findAll('.range-btn')
    expect(buttons).toHaveLength(3)
  })

  it('shows range values', () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [],
        disabled: false,
      },
    })
    expect(wrapper.text()).toContain('0')
    expect(wrapper.text()).toContain('30')
    expect(wrapper.text()).toContain('60')
    expect(wrapper.text()).toContain('100')
  })

  it('emits select event when range is clicked', async () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [],
        disabled: false,
      },
    })
    const firstButton = wrapper.findAll('.range-btn')[0]
    await firstButton.trigger('click')
    expect(wrapper.emitted('select')).toBeTruthy()
    expect(wrapper.emitted('select')![0]).toEqual([0])
  })

  it('marks previously guessed ranges as wrong', () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [{ low: 30, high: 60 }],
        disabled: false,
      },
    })
    const buttons = wrapper.findAll('.range-btn')
    expect(buttons[1].classes()).toContain('guessed-wrong')
    expect(buttons[0].classes()).not.toContain('guessed-wrong')
  })

  it('disables buttons when disabled prop is true', () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [],
        disabled: true,
      },
    })
    const buttons = wrapper.findAll('.range-btn')
    buttons.forEach((btn) => {
      expect(btn.attributes('disabled')).toBeDefined()
    })
  })

  it('does not emit select on guessed-wrong range click', async () => {
    const wrapper = mount(RangeSelector, {
      props: {
        ranges: defaultRanges,
        previousGuesses: [{ low: 0, high: 30 }],
        disabled: false,
      },
    })
    const firstButton = wrapper.findAll('.range-btn')[0]
    await firstButton.trigger('click')
    expect(wrapper.emitted('select')).toBeFalsy()
  })
})
