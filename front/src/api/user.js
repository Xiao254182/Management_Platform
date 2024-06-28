import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

export function getUserInfo() {
  return request({
    url: '/profile'
  })
}

/**
 * 更新密码
 * **/
export function updatePassword(data) {
  return request({
    url: '/user/updatePass',
    method: 'put',
    data
  })
}
