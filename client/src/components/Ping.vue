<template>
  <div>
    <p v-bind:style="{fontSize: '30px'}">{{ msg }}</p>
    <button v-bind:style="{width: 50}" v-on:click="getNumber('now')">Now</button>
    <input v-model="day" placeholder="What time?">
    <button v-on:click="getNumber('time')">Go</button>
    <p>{{ number }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
      number: '',
      day: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getNumber(when) {
      const path = 'http://localhost:5000/';
      let time = 0;
      if (when === 'now') {
        time = new Date().getHours();
      } else {
        time = this.day;
      }
      axios.post(path + time, time)
        .then((res) => {
          this.number = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
