import request from '@/utils/request'

/**
 * 获取消息列表
 * **/

export function getMessageList() {
  return request({
    url: '/home/notice'
  })
}
