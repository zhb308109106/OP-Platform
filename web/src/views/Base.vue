<template>
  <el-container style="height: 100vh; margin-top: 0px; border: 1px solid #eee">
  <el-aside width="200px" style="background: #545c64">
    <el-menu default-active="1" background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span slot="title">CMDB管理</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
  <el-container>
  <el-header style="text-align: right; font-size: 12px; background: #545c64">
      <span><font color="#fff">{{user}},欢迎您！</font></span>
      <el-button type="info" @click="logout">退出</el-button>
  </el-header>

  <el-main style="align-items: stretch;">
       <el-table
    :data="DeviceList">
    <el-table-column prop="system_name"
      label="系统名">
    </el-table-column>
    <el-table-column prop="server_name"
      label="服务器名">
    </el-table-column>
     <el-table-column prop="server_ip"
      label="服务器IP">
    </el-table-column>
     <el-table-column prop="app_admin"
      label="应用管理员">
    </el-table-column>
     <el-table-column prop="server_type"
      label="服务器类型">
    </el-table-column>
     <el-table-column prop="asset_ownership"
      label="资产归属">
    </el-table-column>
    <el-table-column prop="admin_pwd" v-if="false">
    </el-table-column>
    <el-table-column>
      <template #header>
         <el-upload
         name="put_file"
         class="upload-demo"
         action="http://192.168.20.127:8000/upload/"
         :show-file-list="false"
         :on-success="handleSuccess"
        >
         <el-button type="primary" size='small'>批量录入</el-button>

        </el-upload>
        <el-input v-model="SearchIp" size="small" placeholder="请输入服务器ip搜索">
        <template #append>
            <el-button tpye="primary" size="small" @click="search(SearchIp)">搜索</el-button>
        </template>
        </el-input>
      </template>
      <template #default="scope">
        <div>
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
          >编辑</el-button
        >
        <el-button size="small" @click="handleSSH(scope.$index, scope.row)"
          >ssh</el-button
        >
        <el-popconfirm confirmButtonText="确定" cancelButtonText="取消" title="确定删除吗？" @confirm="handleDelete(scope.$index, scope.row)"
          @cancel="cancelEvent">
        <template #reference>
        <el-button
          size="small"
          type="danger"
          >删除</el-button
        >
        </template>
        </el-popconfirm>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <div class="block">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="CurrentPage"
      :page-sizes="[50, 100, 150, 200]"
      :page-size="PageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="DeviceCount">
    </el-pagination>
  </div>
    </el-main>
  </el-container>

</el-container>
 <el-dialog v-model="dialogFormVisible" title="服务器详情">
    <el-form :model="device">
      <el-form-item label="系统名称" :label-width="formLabelWidth">
        <el-input v-model="device.system_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器名称" :label-width="formLabelWidth">
        <el-input v-model="device.server_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器IP" :label-width="formLabelWidth">
        <el-input v-model="device.server_ip" autocomplete="off" />
      </el-form-item>
      <el-form-item label="应用管理员" :label-width="formLabelWidth">
        <el-input v-model="device.app_admin" autocomplete="off" />
      </el-form-item>
      <el-form-item label="资产归属" :label-width="formLabelWidth">
        <el-input v-model="device.asset_ownership" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器类型" :label-width="formLabelWidth">
        <el-input v-model="device.server_type" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="UpdateDevice(device)">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

</template>



  
      
   
  


<style lang="less" scoped>
.el-header {
    background-color: #b3c0d1;
    color: var(--el-text-color-primary);
    line-height: 60px;
  }

  .el-aside {
    color: var(--el-text-color-primary);
  }
</style>

<script>
  import axios from 'axios';
  import {ref} from 'vue';
  import { UploadInstance, UploadProps, UploadRawFile } from 'element-plus';
  
  import {Base64} from 'js-base64';
  let token = localStorage.getItem('token')
  let search_page = 1
  let search_size= 50
  export default {
    data() {
      return {
        DeviceCount: 0,
        CurrentPage: 1,
        PageSize: 100,
        DeviceList: [],
        SearchIp: '',
        dialogFormVisible: ref(false),
        device: {
          'server_name': '',
          'system_name': '',
          'server_ip': '',
          'id': 0,
          'server_type': '',
          'asset_ownership': '',
          'app_admin': ''
        },
        user: localStorage.getItem('user'),
        upload: '',
      }
    },
    methods: {
      logout () {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.$router.push('/login')
      },
      handleSuccess(uploadFile, uploadFiles){
         alert('success!')
      },
      checkTokenExpired(token){
        if(JSON.parse(token).expires) {

        // 获取当前时间
        
        let now = Date.now();
        if(now  > JSON.parse(token).expires) {
            return false;
        } else{
         return true;

        }
       }
      },
      get_Device(page,size){
        const token = localStorage.getItem('token')
        if(this.checkTokenExpired(token)){
          
          const auth = 'Token ' + JSON.parse(token).value; 
          const header = {'Authorization':auth}
          axios.get('http://192.168.20.127:8000/api/device/',{'headers': header,'params':{'page': page, 'size': size}}).then((response)=>{
             this.DeviceCount=response.data.count;
             this.DeviceList=response.data.results;
             this.PageSize=size;
             this.CurrentPage=page;
          }).catch((err)=>{
            console.log(err);
          })
        }
      },
      get_Device_ByIP(ip){
        const token = localStorage.getItem('token')
        if(this.checkTokenExpired(token)){
            const auth = 'Token ' + JSON.parse(token).value;
            const header = {'Authorization':auth}
            axios.get('http://192.168.20.127:8000/api/device/',{'headers': header,'params':{'server_ip': ip,'page':1,'size':200}}).then((response)=>{
               this.DeviceCount=response.data.count;
               this.DeviceList=response.data.results;
               this.PageSize=200;
               this.CurrentPage=1;
              }).catch((err)=>{
              console.log(err);
            })
         }
      },
      handleEdit(index, row) {
        this.dialogFormVisible = ref(true)
        this.device.server_name=row.server_name
        this.device.server_ip=row.server_ip
        this.device.system_name=row.system_name
        this.device.id = row.id 
        this.device.app_admin = row.app_admin
        this.device.server_type = row.server_type
        this.device.asset_ownership = row.asset_ownership
      },
      handleSSH(index,row){
         const url='http://192.168.20.127:8888/?hostname='+row.server_ip+'&username=root&password='+Base64.encode(row.admin_pwd)
         window.open(url,'_blank')

      },
      UpdateDevice(row) {
        const token = localStorage.getItem('token')
        const auth = 'Token ' + JSON.parse(token).value;
        const header = {'Authorization':auth,'Content-Type': 'multipart/form-data'}
        let data = new FormData();
        data.append('server_ip',row.server_ip);
        data.append('server_name',row.server_name);
        data.append('system_name',row.system_name);
        data.append('app_admin',row.app_admin);
        data.append('server_type', row.server_type);
        data.append('asset_ownership',row.asset_ownership);
        axios.put('http://192.168.20.127:8000/api/device/'+row.id+'/',data,{'headers': header}).then((response)=>{
           this.get_Device(1,50);

        }).catch((err)=>{
        console.log(err);
        })
        this.dialogFormVisible = ref(false)

      },
      handleDelete(index, row) {
        const token = localStorage.getItem('token')
        const auth = 'Token ' + JSON.parse(token).value;
        const header = {'Authorization':auth}
        axios.delete('http://192.168.20.127:8000/api/device/'+row.id+'/',{'headers': header}).then((response)=>{
          this.get_Device(1,50);

        }).catch((err)=>{
        console.log(err);
        })
      },
      search(val){
        this.get_Device_ByIP(val)       
      },
      handleSizeChange(val) {
        this.PageSize=val
        this.get_Device(this.CurrentPage,this.PageSize)
      },
      handleCurrentChange(val) {
        this.CurrentPage=val
        this.get_Device(this.CurrentPage,this.PageSize)
      }
    },
    mounted(){ 
      if (token && Object.keys(token).length!=0) {
        if(this.checkTokenExpired(token)){
           this.get_Device(1,50);
        } else{
         localStorage.removeItem('token');
         localStorage.removeItem('user');
         this.$router.push('/login');
        }

      }else{
         if(localStorage.getItem('token') && this.checkTokenExpired(localStorage.getItem('token'))){
            this.get_Device(1,50);
         }else {
           this.$router.push('/login');
         }
      }
       
    }
    

  }
</script>
