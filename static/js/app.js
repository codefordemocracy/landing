var mailchimp = {}
function getMailchimp(json) {
  mailchimp = json
}

/* Initialize Elements */

new Vue({
  el: '#navbar',
  data: {
    open: false
  }
})

new Vue({
  el: '#subscribe',
  data: {
    form: {
      b_b4403b081b3c5fd183e8f1f60_0a70f9292d: null,
      EMAIL: null,
      ORIGIN: 'Landing'
    },
    error: false,
    success: false
  },
  methods: {
    subscribe() {
      var self = this
      this.error = false
      this.$http.jsonp('https://codefordemocracy.us15.list-manage.com/subscribe/post-json?u=b4403b081b3c5fd183e8f1f60&id=0a70f9292d&c=getMailchimp', {
        params: this.form
      })
      .catch(function(response) {
        if (mailchimp.msg.includes('already subscribed') || mailchimp.result == 'success') {
          self.success = true
        } else {
          self.error = true
          console.error(mailchimp)
        }
      })
    }
  }
});
