webpackJsonp([0],{25:function(t,e,n){n(85);var a=n(24)(n(70),n(96),"data-v-69cbbc0c",null);t.exports=a.exports},70:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){var t=this;return{total:0,columns:[{title:"发送者",key:"sender",width:120},{title:"文章",key:"title",render:function(t,e){var n=e.row;return t("a",{attrs:{href:"/bot/article?id="+n.id,target:"_blank"}},n.title)}},{title:"时间",key:"created_at",width:100},{title:"操作",width:250,key:"action",render:function(e,n){var a=n.row;return e("div",[e("Button",{props:{type:"text"},on:{click:function(){t.sendToCutt(a)}}},"发到发稿箱"),e("Button",{props:{type:"text"},on:{click:function(){t.$router.push({name:"article-editor",params:{uid:a.id}})}}},"编辑"),e("Button",{props:{type:"text"},on:{click:function(){t.removeArticle(a)}}},"删除")])}}],data:[]}},computed:{currentPage:function(){return this.$route.params.page||1}},methods:{sendToCutt:function(t){this.$http.post()},removeArticle:function(t){var e=this;e.$Modal.confirm({content:"确认要删除【"+t.title+"】吗？",onOk:function(){e.$http.post("/bot/article/remove",{id:t.id}).then(function(){e.data.splice(e.data.indexOf(t),1)})}})},changePage:function(t){this.$router.push({name:"bot-articles-page",params:{page:t}})}},mounted:function(){var t=this;this.$http.get("/bot/articles",{params:{name:this.$route.params.bot,page:this.currentPage-1}}).then(function(e){t.data=e.data.articles,t.total=e.data.total})}}},85:function(t,e){},96:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("Table",{attrs:{columns:t.columns,data:t.data}}),t._v(" "),n("Page",{staticStyle:{"padding-top":"10px"},attrs:{total:t.total,current:t.currentPage,"show-elevator":"",size:"small"},on:{"on-change":t.changePage}})],1)},staticRenderFns:[]}}});