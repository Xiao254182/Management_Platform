import request from '@/utils/request'

/**
 * 获取员工列表
 * **/

export function getEmployeeList(params) {
  return request({
    url: '/user',
    params // 地址参数 查询参数
  })
}

/**
 * 导出员工的excel
 * **/

export function exportEmployee() {
  return request({
    url: '/user/export',
    // 改变接收数据的类型
    responseType: 'blob' // 使用blob接收二进制文件流
  })
}

/**
 * 下载员工导入模版
 * **/

export function getExportTemplate() {
  return request({
    url: '/user/import/template',
    responseType: 'blob' // 二进制文件流
  })
}

/**
 * 上传用户的excel
 *
*/
export function uploadExcel(data) {
  return request({
    url: '/user/import',
    method: 'post',
    data // form-data类型 因为要上传文件类型
  })
}
/**
 * 删除员工
 * **/

export function delEmployee(id) {
  return request({
    method: 'delete',
    url: `/user/${id}`
  })
}

/**
 * 新增员工
 * ***/

export function addEmployee(data) {
  return request({
    url: '/user',
    method: 'post',
    data
  })
}

/**
 *  获取员工详情
 * **/

export function getEmployeeDetail(id) {
  return request({
    url: `/user/${id}`
  })
}

/**
 * 更新员工
 * ***/

export function updateEmployee(data) {
  return request({
    url: `/user/${data.id}`,
    method: 'put',
    data
  })
}

/**
 * 获取可用的角色
 * **/

export function getEnableRoleList() {
  return request({
    url: '/role/list/enabled'
  })
}

/**
 * 分配员工角色
 * ***/

export function assignRole(data) {
  return request({
    url: '/user/assignRoles',
    method: 'put',
    data
  })
}
