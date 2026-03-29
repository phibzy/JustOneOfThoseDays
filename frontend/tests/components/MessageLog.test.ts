import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MessageLog from '../../src/components/MessageLog.vue'

describe('MessageLog', () => {
  it('shows empty state when no messages', () => {
    const wrapper = mount(MessageLog, {
      props: { messages: [] },
    })
    expect(wrapper.text()).toContain('No activity yet')
  })

  it('renders messages', () => {
    const wrapper = mount(MessageLog, {
      props: {
        messages: ['Alice guessed correctly!', 'New round started'],
      },
    })
    expect(wrapper.text()).toContain('Alice guessed correctly!')
    expect(wrapper.text()).toContain('New round started')
  })

  it('renders correct number of list items', () => {
    const wrapper = mount(MessageLog, {
      props: {
        messages: ['Msg 1', 'Msg 2', 'Msg 3'],
      },
    })
    const items = wrapper.findAll('.message-log li')
    expect(items).toHaveLength(3)
  })
})
