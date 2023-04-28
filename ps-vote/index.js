
// document.addEventListener('readystatechange', event => {

//   // When window loaded ( external resources are loaded too- `css`,`src`, etc...) 
//   if (event.target.readyState === "complete") {


//     const app = Vue.createApp({
//       delimiters: ['[[', ']]'],
//       data() {
//         return {
//           message: '',
//           inputText: '',
//           page1: true,
//           page2: false,
//           page3: false,
//           isOpen: false,
//           array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
//         }
//       },
//       computed: {

//       },
//       methods: {
//         async renderLong() {
//           this.message = 'Longitude'
//           this.page1 = false
//           this.page2 = true

//           fetch('http://erp.localhost:8000/api/method/get_employees_long', {
//             mode: 'no-cors',
//             method: 'GET',
//             headers: {
//               accept: 'application/json',
//             },
//           }).then(r => r)
//             .then(r => {
//               console.log(r);
//             })
//         },

//         async renderLat() {
//           this.message = 'Latitude'
//           this.page1 = false
//           this.page2 = true

//           fetch('http://erp.localhost:8000/api/method/get_employees_lat', {
//             mode: 'no-cors',
//             method: 'GET',
//             headers: {
//               accept: 'application/json',
//             },
//           }).then(r => r.json())
//             .then(r => {
//               console.log(r);
//             })

//           // console.log(response.status);

//           // const result = await response.json();
//           // console.log(result);
//         },

//         handleNav() {
//           this.page1 = true
//           this.page2 = false
//         },

//         handleSearch(e) {
//           e.preventDefault()
//           console.log(inputText);
//         },

//         handleVote(id) {
//           console.log(`You voted for ${id}`);
//           this.isOpen = false
//         }
//       }
//     })

//     app.mount('#app')

//   }
// });