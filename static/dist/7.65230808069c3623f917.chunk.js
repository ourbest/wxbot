webpackJsonp([7],{62:function(t,e,a){a(81);var s=a(24)(a(73),a(92),"data-v-0a1fae6b",null);t.exports=s.exports},73:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{autoAccept:!1,crawlerArticles:!1,autoSend:!1,info:"",appId:null}},computed:{bot:function(){return this.$route.params.bot}},methods:{changeAccept:function(){var t=this;this.$http.post("/bot/config",{name:this.bot,key:"auto_accept",value:!!this.autoAccept}).then(function(e){t.$Message.info(e.data.message)})},changeCrawlerArticles:function(){var t=this;this.$http.post("/bot/config",{name:this.bot,key:"crawler_articles",value:!!this.crawlerArticles}).then(function(e){t.$Message.info(e.data.message)})},changeAutoSend:function(){var t=this;this.$http.post("/bot/config",{name:this.bot,key:"auto_send",value:!!this.autoSend}).then(function(e){t.$Message.info(e.data.message)})},saveAppId:function(){var t=this;this.$http.post("/bot/config",{name:this.bot,key:"app_id",value:this.appId}).then(function(e){t.$Message.info(e.data.message)})},logoutBot:function(){var t=this;this.$http.get("/bot/logout",{params:{name:this.bot}}).then(function(){t.$router.push("/")})},setAsMaster:function(){var t=this;this.$http.get("/bot/master/assign",{params:{name:this.bot}}).then(function(e){0===e.data.code?(t.$store.commit("reload"),t.$store.commit("login",""),t.$router.push("/")):t.$Message.info(e.data.message)})}},mounted:function(){var t=this;""===this.bot?this.$router.push("/"):this.$http.get("/bot/info",{params:{name:this.bot}}).then(function(e){t.info=e.data.friends,t.autoAccept=e.data.config.auto_accept,t.appId=e.data.config.app_id,t.crawlerArticles=e.data.config.crawler_articles})}}},81:function(t,e){},92:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"settings"},[a("Alert",{attrs:{type:"info"}},[t._v("\n            设置\n            "),a("span",{slot:"desc"},[a("ul",[a("li",[t._v("自动接收好友"),a("span",{staticClass:"switch"},[a("i-switch",{on:{"on-change":t.changeAccept},model:{value:t.autoAccept,callback:function(e){t.autoAccept=e},expression:"autoAccept"}})],1)]),t._v(" "),a("li",[t._v("抓取公众号文章"),a("span",{staticClass:"switch"},[a("i-switch",{on:{"on-change":t.changeCrawlerArticles},model:{value:t.crawlerArticles,callback:function(e){t.crawlerArticles=e},expression:"crawlerArticles"}})],1)]),t._v(" "),a("li",[t._v("自动发送抓取的文章"),a("span",{staticClass:"switch"},[a("i-switch",{on:{"on-change":t.changeAutoSend},model:{value:t.autoSend,callback:function(e){t.autoSend=e},expression:"autoSend"}})],1)]),t._v(" "),a("li",[t._v("AppID"),a("span",{staticClass:"switch"},[a("Row",{attrs:{type:"flex"}},[a("i-col",[a("i-input",{model:{value:t.appId,callback:function(e){t.appId=e},expression:"appId"}})],1),a("i-col",[a("Button",{on:{click:t.saveAppId}},[t._v("保存")])],1)],1)],1)])])])])],1),t._v(" "),a("pre",[t._v(t._s(t.info))]),t._v(" "),a("Button",{attrs:{type:"primary"},on:{click:t.logoutBot}},[t._v("注销")]),t._v(" "),a("Button",{attrs:{type:"error"},on:{click:t.setAsMaster}},[t._v("设置为监控人")])],1)},staticRenderFns:[]}}});