import request from '@/utils/request'
// 获取考勤列表
export function getAttendancesList(params) {
  return request({
    url: '/attendances',
    params
  })
}

export function updateAttendance(data) {
  return request({
    url: `/attendances/${data.userId}`,
    method: 'put',
    data
  })
}