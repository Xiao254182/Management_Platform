<template>
  <div v-loading="loading" class="dashboard-container">
    <div class="app-container">
      <!-- 工具栏 -->
      <page-tools :show-before="true" />
      <el-card class="hr-block">
        <el-form
          ref="formData"
          :model="formData"
          label-width="120px"
          class="formInfo"
        >
          <el-form-item label="部门:">
            <el-checkbox-group
              v-model="formData.deptID"
              @change="handleDepartmentChange"
            >
              <el-checkbox
                v-for="item in departments"
                :key="item.id"
                ref="deptTree"
                :label="item.name"
                node-key="id"
                :data="depts"
                :props="defaultProps"
                default-expand-all
                :expand-on-click-node="false"
                highlight-current
                @current-change="selectNode"
              >
                {{ item.name }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="考勤状态：">
            <el-checkbox-group
              v-model="formData.stateID"
              @change="handleStateChange"
            >
              <el-checkbox
                v-for="item in stateData.holidayType"
                :key="item.id"
                :label="item.id"
                :value="item.id"
              >
                {{ item.value }}
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </el-card>
      <!-- 考勤数据 -->
      <el-card class="hr-block">
        <!-- 考勤列表 -->
        <div
          style="
            width: 100%;
            position: relative;
            overflow-x: auto;
            overflow-y: hidden;
          "
        >
          <div style="width: 3000px">
            <table
              border="0"
              align="center"
              cellpadding="0"
              cellspacing="0"
              class="tableInfo"
            >
              <tr>
                <th width="50">序号</th>
                <th width="100">姓名</th>
                <th width="100">工号</th>
                <th width="200">部门</th>
                <th width="100">手机</th>
                <th v-for="(it, ind) in monthOfReport" :key="ind" width="110">
                  {{ attendInfo.month }}/{{ ind + 1 }}
                </th>
              </tr>
              <tr v-for="(item, index) in list" :key="item.id">
                <td width="50">{{ index }}</td>
                <td width="100">{{ item.username }}</td>
                <td width="100">{{ item.workNumber }}</td>
                <td width="200">{{ item.departmentName }}</td>
                <td width="100">{{ item.mobile }}</td>
                <td
                  v-for="(it, ind) in item.attendanceRecord"
                  :key="ind"
                  width="110"
                  @click="showChangeDialog(item, ind, it)"
                >
                  <span v-if="it.adtStatu === 1">√</span>
                  <span v-if="it.adtStatu === 2">旷工</span>
                  <span v-if="it.adtStatu === 3">迟到</span>
                  <span v-if="it.adtStatu === 4">早退</span>
                  <span v-if="it.adtStatu === 5">请假</span>
                  <span v-if="it.adtStatu === 6">补假</span>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <el-dialog :visible.sync="centerDialogVisible" width="30%" center>
          <span slot="title" style="color: #fff"
            >{{ attendInfo.name }} {{ attendInfo.month }}/{{
              attendInfo.getDate
            }}（实际工作日考勤方案）</span
          >
          <div class="attenInfo">
            <p class="check">
              <el-radio-group v-model="modifyData.adtStatu">
                <el-radio
                  v-for="item in stateData.vacationtype"
                  :key="item.id"
                  :label="item.id"
                  :value="item.id"
                  >{{ item.name }}</el-radio
                >
              </el-radio-group>
            </p>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="btnOK">确定</el-button>
            <el-button @click="centerDialogVisible = false">取消</el-button>
          </span>
        </el-dialog>
        <!-- 分页组件 -->
        <el-row
          type="flex"
          align="middle"
          justify="center"
          style="height: 60px"
        >
          <el-pagination
            :page-size="page.pagesize"
            :current-page="page.page"
            layout="prev, pager, next"
            :total="page.total"
            @current-change="pageChange"
          />
        </el-row>
      </el-card>
    </div>
    <el-card>
      <!-- 提醒组件 -->
      <el-dialog
        title="提醒"
        :visible.sync="tipsDialogVisible"
        width="280px"
        center
      />
      <!-- 设置组件 -->
    </el-card>
  </div>
</template>

<script>
import { getAttendancesList, updateAttendance } from "@/api/attendance";
import { getDepartment } from "@/api/department";

export default {
  name: "Attendances",
  data() {
    return {
      queryParams: {
        departmentId: null,
      },
      list: [],
      selectData: [],
      stateData: {
        // 假期类型
        holidayType: [
          {
            id: "1",
            value: "正常",
            isEnable: false,
          },
          {
            id: "2",
            value: "旷工",
            isEnable: false,
          },
          {
            id: "3",
            value: "迟到",
            isEnable: false,
          },
          {
            id: "4",
            value: "早退",
            isEnable: false,
          },
          {
            id: "5",
            value: "请假",
            isEnable: false,
          },
          {
            id: "6",
            value: "补假",
            isEnable: false,
          },
        ],
        vacationtype: [
          {
            id: "1",
            name: "正常",
          },
          {
            id: "2",
            name: "旷工",
          },
          {
            id: "3",
            name: "迟到",
          },
          {
            id: "4",
            name: "早退",
          },
          {
            id: "5",
            name: "请假",
          },
          {
            id: "6",
            name: "补假",
          },
          {
            id: "7",
            name: "",
          },
        ],
      },
      departments: [],
      total: 100,
      attendanceRecord: "",
      monthOfReport: "",
      centerDialogVisible: false,
      tipsDialogVisible: false,
      month: "",
      yearMonth: "",
      loading: false,
      attendInfo: {
        month: "",
        getDate: "",
        getInfo: "",
        name: "",
        counts: "",
        tobeTaskCount: "",
      },
      formData: {
        page: 1,
        pagesize: 10,
        keyword: this.keyword,
        deptID: [], // 性别
        stateID: [], // 修改为数组
      },
      page: {
        page: 1,
        pagesize: 10,
        total: 0,
      },
      modifyData: {
        userId: "",
        day: "",
        adtStatu: "",
      },
    };
  },
  // 创建完毕状态
  created() {
    // this.updateAttendance() // 更新考勤状态
    this.getAttendancesList(); // 获取考勤列表
    this.getDepartment(); // 获取考勤列表
  },
  methods: {
    // 暂时不处理
    handleSub() {
      this.tipsDialogVisible = false;
      this.$message.success("提醒成功");
    },
    handleTip() {
      this.tipsDialogVisible = true;
    },
    // 设置
    handleSet() {
      this.$refs.set.dialogFormV();
    },
    // 弹框关闭
    handleCloseModal() {
      this.$refs.set.dialogFormH();
    },
    // 获取组织列表
    async getDepartment() {
      this.departments = await getDepartment();
    },

    // 初始化数据
    async getAttendancesList() {
      this.loading = true;
      const { data, monthOfReport, tobeTaskCount } = await getAttendancesList({
        ...this.page,
        ...this.queryParams,
      });
      this.list = data.rows; // 当前记录
      this.page.total = data.total; // 总条数
      this.attendInfo.counts = data.total;
      this.attendInfo.month = monthOfReport;
      this.attendInfo.tobeTaskCount = tobeTaskCount;

      var date = new Date();
      var year = date.getFullYear();
      const month = monthOfReport;
      var d = new Date(year, month, 0); // 获取月份
      this.monthOfReport = d.getDate(); // 获取日期
      this.yearMonth = year + ("" + month < 10 ? "0" + month : month);
      this.month = monthOfReport;
      this.loading = false;
    },
    // 确定修改
    async btnOK() {
      await updateAttendance(this.modifyData);
      this.$message.success("更新成功");
      this.centerDialogVisible = false;
      this.getAttendancesList(); // 成功之后 重新拉取数据
    },
    // 页码改变
    pageChange(page) {
      this.page.page = page;
      this.getAttendancesList(); // 获取数据
    },
    showChangeDialog(item, id, it) {
      this.modifyData.userId = item.id;
      this.modifyData.day = it.day;
      this.modifyData.departmentId = item.departmentId;
      this.modifyData.adtStatu = it.adtStatu + ""; // 数字转成字符串

      if (it.adtStatu !== "") {
        this.attendInfo.getDate = parseInt(id + 1);
        this.attendInfo.getInfo = it.adtStatu;
        this.attendInfo.name = item.name;
        this.centerDialogVisible = true;
      }
    },
    // 处理部门选择变化
    async handleDepartmentChange() {
      this.page.page = 1; // 重置页码
      this.queryParams.departmentName = this.formData.deptID.join(","); // 将选中的部门ID拼接成字符串
      this.loading = true;
      const { data, monthOfReport, tobeTaskCount } = await getAttendancesList({
        ...this.page,
        ...this.queryParams,
      });
      this.list = data.rows; // 当前记录
      this.page.total = data.total; // 总条数
      this.attendInfo.counts = data.total;
      this.attendInfo.month = monthOfReport;
      this.attendInfo.tobeTaskCount = tobeTaskCount;
      this.loading = false;
    },
    // 处理考勤状态选择变化
    async handleStateChange() {
      this.page.page = 1; // 重置页码
      this.queryParams.stateID = this.formData.stateID.join(","); // 将选中的考勤状态ID拼接成字符串
      this.loading = true;
      const { data, monthOfReport, tobeTaskCount } = await getAttendancesList({
        ...this.page,
        ...this.queryParams,
      });
      this.list = data.rows; // 当前记录
      this.page.total = data.total; // 总条数
      this.attendInfo.counts = data.total;
      this.attendInfo.month = monthOfReport;
      this.attendInfo.tobeTaskCount = tobeTaskCount;
      this.loading = false;
    },
  },
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.tableInfo {
  line-height: 36px;
  border: solid 1px #ebeef5;
  border-right: 0 none;
  border-bottom: 0 none;
  tr {
    th {
      height: 50px;
      text-align: center;
      border-right: solid 1px #ebeef5;
      border-bottom: solid 1px #ebeef5;
      border-bottom: 2px solid #e8e8e8;
      background: #fafafa;
      min-width: 100px;
    }
    td {
      height: 36px;
      text-align: center;
      border-right: solid 1px #ebeef5;
      border-bottom: solid 1px #ebeef5;
    }
  }
}

.attenInfo {
  p {
    &.check {
      padding: 20px 0 0;
    }
    .el-radio {
      display: inline-block;
      width: 60px;
      padding: 5px 0;
    }
  }
}
</style>
