webpackJsonp([4],{109:function(t,o){t.exports={render:function(){var t=this,o=t.$createElement,r=t._self._c||o;return r("Row",[r("Form",{attrs:{width:500}},[r("Row",{attrs:{gutter:5}},[r("i-col",{attrs:{span:12}},[r("Form-Item",{attrs:{label:"密码","label-width":100}},[r("i-input",{attrs:{type:"password",placeholder:"请输入密码"},model:{value:t.password,callback:function(o){t.password=o},expression:"password"}})],1)],1),t._v(" "),r("i-col",{attrs:{span:4}},[r("Form-Item",[r("Button",{attrs:{type:"primary"},on:{click:t.login}},[t._v("登录")])],1)],1)],1)],1)],1)},staticRenderFns:[]}},74:function(t,o,r){r(95);var s=r(11)(r(87),r(109),"data-v-3d958102",null);t.exports=s.exports},87:function(t,o,r){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.default={data:function(){return{password:""}},methods:{login:function(){var t=this;""!==this.password&&this.$http.post("/bot/login",{pwd:this.password}).then(function(o){o.data.error||(t.$store.commit("login"),t.$router.push("/"))})}}}},95:function(t,o){}});