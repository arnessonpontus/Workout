<template>
  <div class="container">
    <h1>How many people are there at the gym?</h1>
    <div>
      <button class="location-button" v-on:click="changeFacility('city')">CITY</button>
      <button class="location-button" v-on:click="changeFacility('ingelsta')">INGELSTA</button>
      <button
      class="location-button" v-on:click="changeFacility('vrinnevi')">VRINNEVI</button>
    </div>
    <button class="submit-btn" v-on:click="getNumber('now')">Now</button>
    <div class="mid-container">
      <div class="specific-time">
        <p>Or choose specific parameters:</p>
        <p>Weekday:</p>
        <input class="input" v-model="day" placeholder="2">
        <p>Date:</p>
        <input class="input" v-model="date" placeholder="17">
        <p>Hour:</p>
        <input class="input" v-model="hour" placeholder="16">
        <p>Month:</p>
        <input class="input" v-model="month" placeholder="3">
        <p>Temp:</p>
        <input class="input" v-model="temp" placeholder="5">
        <p>Rain:</p>
        <input class="input" v-model="rain" placeholder="2">
        <p>Sun:</p>
        <input class="input" v-model="sun" placeholder="0">
        <button class="submit-btn" v-on:click="getNumber('hour')">Go</button>
      </div>
      <b class="number">{{ number }}</b>
    </div>
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
      date: '',
      hour: '',
      month: '',
      temp: '',
      rain: '',
      sun: '',
      location: '',
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
    changeFacility() {
    },
    getNumber(when) {
      this.number = '...';
      const path = 'http://localhost:5000/';
      const weekday = this.day;
      const dateNum = this.date;
      // eslint-disable-next-line
      console.log(weekday);
      let time = 0;
      const monthNum = this.month;
      const degree = this.temp;
      const rainNum = this.rain;
      const sunNum = this.sun;
      if (when === 'now') {
        time = new Date().getHours();
      } else {
        time = this.hour;
      }
      // eslint-disable-next-line
      axios.post(`${path + '?' + 'weekday=' + weekday + '&' + 'dateNum=' + dateNum + '&' + 'time=' + time + '&' + 'month=' + monthNum + '&' + 'degree=' + degree + '&' + 'rainNum=' + rainNum + '&' + 'sunNum=' + sunNum}`)
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
