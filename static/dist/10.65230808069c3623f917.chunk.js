webpackJsonp([10],{59:function(t,e,s){s(84);var a=s(24)(s(69),s(95),"data-v-37547bf4",null);t.exports=a.exports},69:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{message:"请扫描二维码",qr:"/bot/qr?t="+(new Date).getTime()}},methods:{getQRStatus:function(){var t=this;this.loading&&this.$http.get("/bot/qr/status").then(function(e){switch(t.message=e.data.message,e.data.code){case"200":t.$store.commit("open",e.data.name);break;case"201":setTimeout(t.getQRStatus,500);break;default:t.qr="/bot/qr?t="+(new Date).getTime(),setTimeout(t.getQRStatus,500)}})}},mounted:function(){this.loading=!0,this.getQRStatus()},beforeDestroy:function(){this.loading=!1}}},84:function(t,e){},95:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"qr"},[s("img",{attrs:{src:t.qr}}),t._v(" "),s("p",[t._v(t._s(t.message))])])},staticRenderFns:[]}}});