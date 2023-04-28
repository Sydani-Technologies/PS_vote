import modal from './modal.vue';
frappe.ready(function () {

  frappe.socketio.init();

  var voteChart = null

  const updateVoteChart = (chart, data) => {
    chart.data.labels = data.labels;
    chart.data.datasets[0].data = data.values;
    chart.update();
  };


  const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
      return {
        message: '',
        inputText: '',
        page1: false,
        page2: false,
        page3: false,
        isOpen: false,
        user: 'Guest',
        vote: '',
        array: [],
        loginForm: { usr: '', pwd: '' },
        loginError: '',
        voteRes: '',
        modalHeader: '',
        startDate: '',
        toDate: '',
        toggleDropdownList: false,
      }
    },
    computed: {

    },
    methods: {
      createChartLabelsAndValues(vote_count) {
        let chartLabels = [];
        let chartValues = [];

        var push_values = (label, value) => {
          chartLabels.push(label);
          chartValues.push(value);
        }

        vote_count.forEach((vote) => {
          push_values(vote.vote_name, vote.votes_today);
        });

        return { 'labels': chartLabels, 'values': chartValues }
      },

      setToggleDropdownList() {
        this.toggleDropdownList = !this.toggleDropdownList
        // console.log(this.toggleDropdownList)
      },

      renderLong() {
        this.toggleDropdownList = !this.toggleDropdownList
        if (this.user === 'Guest') {
          this.isOpen = true
          this.modalHeader = 'You are not Logged in!!'
          this.vote = 'You have to log in with your email and password to vote'
        } else {
          this.message = 'Longitude'
          this.page1 = false
          this.page2 = true
          this.page3 = false

          frappe.call({ method: 'sydani.www.ps-vote.index.get_employee', args: { ps: 'Longitude' } })
            .then((res) => {
              if (res.message.success_key == 0) {
                this.isOpen = true
                this.modalHeader = 'Unable to get employees'
                this.vote = err.message
              } else if (res.message.success_key == 1) {
                this.array = res.message.employees;
              }
            })
        }
      },

      async renderLat() {
        this.toggleDropdownList = !this.toggleDropdownList
        if (this.user === 'Guest') {
          this.isOpen = true
          this.modalHeader = 'You are not Logged in!!'
          this.vote = 'You have to log in with your email and password to vote'
        } else {
          this.message = 'Latitude'
          this.page1 = false
          this.page2 = true
          this.page3 = false

          frappe.call({ method: 'sydani.www.ps-vote.index.get_employee', args: { ps: 'Latitude' } })
            .then((res) => {
              if (res.message.success_key == 0) {
                this.isOpen = true
                this.modalHeader = 'Unable to get employees'
                this.vote = err.message
              } else if (res.message.success_key == 1) {
                this.array = res.message.employees;
              }
            })
        }
      },

      renderComb() {
        this.toggleDropdownList = !this.toggleDropdownList
        if (this.user === 'Guest') {
          this.isOpen = true
          this.modalHeader = 'You are not Logged in!!'
          this.vote = 'You have to log in with your email and password to vote'
        } else {
          this.message = 'Combined'
          this.page1 = false
          this.page2 = true
          this.page3 = false

          frappe.call({ method: 'sydani.www.ps-vote.index.get_employee', args: { ps: '' } })
            .then((res) => {
              if (res.message.success_key == 0) {
                this.isOpen = true
                this.modalHeader = 'Unable to get employees'
                this.vote = err.message
              } else if (res.message.success_key == 1) {
                this.array = res.message.employees;
              }
            })
        }
      },

      handleNav() {
        this.page1 = true
        this.page2 = false
        this.page3 = false
      },

      handleSearch(e) {
        e.preventDefault()
        frappe.call({
          method: 'sydani.www.ps-vote.index.search_employee', args: {
            query: this.inputText,
            ps: this.message
          }
        })
          .then((res) => {
            if (res.message.success_key == 0) {
              console.log(res.message);
            } else if (res.message.success_key == 1) {
              let data = res.message.message.employees
              console.log(data);
              this.array = data
            }
          })
      },

      loginUser() {
        frappe.call({ method: 'sydani.www.ps-vote.index.login', args: this.loginForm })
          .then((res) => {
            if (res.message.success_key == 0) {
              this.loginError = "Login Failed";
              setTimeout(() => {
                this.loginError = "";
              }, 3000)
            } else if (res.message.success_key == 1) {
              this.user = res.message.user;
              this.page1 = true
              this.page2 = false
              this.page3 = false
            }
          })
      },

      handleDatePick() {
        console.log('startDate:', this.startDate);
        console.log('startDate:', this.toDate);

        this.getVotes()
      },

      async getVotes() {
        this.page3 = true
        this.page2 = false

        try {
          const res = await frappe.call({
            method: 'sydani.www.ps-vote.index.get_result',
            args: {
              team: (this.message === 'Combined' ? 'Combined' : this.message),
              from_date: this.startDate ? this.startDate : '',
              to_date: this.toDate ? this.toDate : ''
            }
          })

          if (res.message.success_key === 1) {
            const votesToday = this.createChartLabelsAndValues(res.message.votes)

            console.log(votesToday);
            console.log(res.message);

            const options = {
              responsive: true,
              plugins: {
                legend: false,
                // title: { display: true, text: `${this.message} PS Votes` },
                // { position: 'bottom' }
              },
              scales: {
                y: { beginAtZero: true, ticks: { precision: 2 } },
                x: { ticks: { autoSkip: true } }
              },
              interaction: {
                mode: 'nearest',
                intersect: true
              },
              animation: {
                duration: 500,
                easing: 'easeOutQuart'
              }
            }
            console.log(votesToday);
            const chartData = {
              labels: votesToday.labels,
              datasets: [
                {
                  label: 'Vote(s)',
                  data: votesToday.values,
                  backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F1937E', '#798C6F', '#8BE4EA', '#C087EA']
                }
              ]
            }

            if (voteChart) {
              updateVoteChart(voteChart, votesToday)
            } else {
              voteChart = new Chart(this.$refs.chartContainer, {
                type: 'bar',
                data: chartData,
                options: options,
              })
            }
          } else {
            this.isOpen = true
            this.modalHeader = 'Unable to get votes'
            this.vote = 'An error has occurred when getting the results, please retry!'
          }
        } catch (error) {
          console.error(error)
          this.isOpen = true
          this.modalHeader = 'Unable to get votes'
          this.vote = 'An error has occurred when getting the results, please retry!'
        }
      },

      handleVote(id) {
        frappe.call({
          method: 'sydani.www.ps-vote.index.cast_vote', args: {
            employee_voted: id, ps: this.message, user_email: this.user
          }
        }).then(res => {
          if (res.message.success_key == 1) {
            this.isOpen = true
            this.vote = `Your have voted for ${id.employee_name} as a PS star for today's session`
            this.modalHeader = 'Your Vote Has Been Recorded!!'
          } else {
            this.isOpen = true
            this.modalHeader = 'Your Vote Was Not Recorded'
            this.vote = `Your have already cast your vote for today's PS session`
          }
        });
      }
    }
  })

  app.mount('#app')

  // })
});


  // const date = new Date()
        // let year = date.getFullYear();
        // let month = date.getMonth() + 1;
        // let day = date.getDate()

        // const actual_date = `${year}-${month}-${day}`

        // let data = {
        //   'voter_name': this.user,
        //   'vote_name': id.employee_name,
        //   'vote_id': id.employee,
        //   'ps': this.message,
        //   'date': actual_date
        // }
        // console.log(data);
