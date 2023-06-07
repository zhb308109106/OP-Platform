<template>
    <div class="loginbBody">
        <div class="loginDiv">
            <div class="login-content">
                <h1 class="login-title">用户登录</h1>
                <el-form :model="loginForm" label-width="100px"
                         :rules="rules" ref="loginForm">
                    <el-form-item label="姓名" prop="name">
                        <el-input  type="text" v-model="loginForm.name"
                                  autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input  type="password" v-model="loginForm.password"
                                  show-password autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="confirm">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
   import axios from 'axios';
   import {ref} from 'vue';
    export default {
        name: "login",
        data(){
            return{
                loginForm:{
                    name:'',
                    password:''
                },
                rules:{
                  name: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 15, message: '用户名长度在 3 到 15 个字符', trigger: 'blur' }
                  ],
                  password: [
                    { required: true, message: '请输密码', trigger: 'blur' },
                    { min: 8, max: 15, message: '密码长度在 8 到 15 个字符', trigger: 'blur' }
                  ]

                }
            }
        },
        methods:{
            confirm(){
              axios.post('http://192.168.20.127:8000/login/', this.loginForm).then(response =>{
              const {result, detail, errorInfo}  = response.data;
              if(result == true){
                 // 登录成功
                 // 设置token
                 localStorage.setItem('user',this.loginForm.name)
                 let startTime = Date.now()
                 let expires = startTime + 1000 * 60 * 60;
                 localStorage.setItem('token', JSON.stringify({value: detail.token, startTime, expires}));
                 // 跳转页面
                 this.$router.push('/');
          }else{
              this.$message({
                  showClose: true,
                  message: errorInfo,
                  type: 'error'
              });
          }
         });
      
        }
        }
    }
</script>

<style scoped >
    .loginbBody {
        width: 100%;
        height: 100%;
        background-color: #B3C0D1;
    }
    .loginDiv {
        position: absolute;
        top: 50%;
        left: 50%;
        margin-top: -200px;
        margin-left: -250px;
        width: 450px;
        height: 330px;
        background: #fff;
        border-radius: 5%;

    }
    .login-title {
        margin: 20px 0;
        text-align: center;
    }
    .login-content {
        width: 400px;
        height: 250px;
        position: absolute;
        top: 25px;
        left: 25px;
    }
</style>

