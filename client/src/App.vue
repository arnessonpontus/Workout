<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  background: linear-gradient( #5c5951 0%, rgb(173, 168, 155) 100%);

  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  min-height: 100vh;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

h1{
  margin: 0 0 0 20;
  color: #ffffff;
  margin-top: 40px;
}

.container{
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.input{
  border-radius: 4px;
}

.content{
  background-color: rgb(212, 235, 227)
}

.location-button{
  background-color: #c03a3a;
  font-size: 100%;
  width: 180px;
  height: 90px;
  margin: 30px;
  border-radius: 5px;
  border-color: #c03a3a;
  color: white;
  cursor: pointer;
}

.mid-container{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap
}

p{
  font-size: 15px;
  margin: 1px
}

.submit-btn{
  height: 40px;
  width: 70px;
  margin-top: 5px;
  border-radius: 5px;
  cursor: pointer;
  background-color: rgb(61, 180, 91);
  border-color: rgb(61, 180, 91);
  color: white;
}
.submit-btn:hover{
  background-color: rgb(183, 243, 181);
  border-color: rgb(183, 243, 181);
}

.specific-time{
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 300px
}

.number{
  color: rgb(255, 255, 255);
  font-size: 38px;
  width: 300px;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
