<template>
  <div class="container">
    <!-- <div class="refresh">🔄</div> -->
    <div class="twodropdowns">
      <div class="dropdown" @change="dropdownOnChange">
        <select v-model="from_place" name="from" class="dropdown-select">
          <option disabled value="">Select Your Location</option>
          <option>TA</option>
          <option>Lanting</option>
          <option>DKU</option>
        </select>
      </div>
      <div style="font-size: 2rem">➡️</div>
      <div class="dropdown" @change="dropdownOnChange">
        <select v-model="to_place" name="to" class="dropdown-select">
          <option disabled value="">Select Your Destination</option>
          <option>TA</option>
          <option>Lanting</option>
          <option>DKU</option>
        </select>
      </div>
    </div>

    <div class="card">
      <div class="description">Next Shuttle</div>
      <div class="time" id="countdown">{{ remainTimeString }}</div>
      <div style="margin-left: auto">*Not Applicable on holidays</div>
    </div>
    <hr />

    <table
      :style="{ display: show_weekday_A }"
      id="weekday_A"
      class="rwd-table"
    >
      <tr>
        <th v-for="stop in shuttle_data['weekday_stops_A']" v-bind:key="stop">
          {{ stop }}
        </th>
      </tr>
      <tr v-for="item in shuttle_data['weekday_A']" v-bind:key="item">
        <td v-for="time in item" v-bind:key="time">{{ time }}</td>
      </tr>
    </table>

    <table
      :style="{ display: show_weekday_B }"
      id="weekday_B"
      class="rwd-table"
    >
      <tr>
        <th v-for="stop in shuttle_data['weekday_stops_B']" v-bind:key="stop">
          {{ stop }}
        </th>
      </tr>
      <tr v-for="item in shuttle_data['weekday_B']" v-bind:key="item">
        <td v-for="time in item" v-bind:key="time">{{ time }}</td>
      </tr>
    </table>

    <table
      :style="{ display: show_weekend_A }"
      id="weekend_A"
      class="rwd-table"
    >
      <tr>
        <th v-for="stop in shuttle_data['weekend_stops_A']" v-bind:key="stop">
          {{ stop }}
        </th>
      </tr>
      <tr v-for="item in shuttle_data['weekend_A']" v-bind:key="item">
        <td v-for="time in item" v-bind:key="time">{{ time }}</td>
      </tr>
    </table>

    <table
      :style="{ display: show_weekend_B }"
      id="weekend_B"
      class="rwd-table"
    >
      <tr>
        <th v-for="stop in shuttle_data['weekend_stops_B']" v-bind:key="stop">
          {{ stop }}
        </th>
      </tr>
      <tr v-for="item in shuttle_data['weekend_B']" v-bind:key="item">
        <td v-for="time in item" v-bind:key="time">{{ time }}</td>
      </tr>
    </table>

    <!-- <a  href="https://www.afdian.net/@hi_keon">
      <img
        id="banner"
        src="https://i.loli.net/2020/07/11/iUh6QFTXMormBnH.png"
        alt=""
      />
    </a> -->
  </div>
</template>

<script>
import shuttle_data from "./assets/shuttle_schedule.json";

export default {
  data: function () {
    return {
      shuttle_data: shuttle_data,
      current_weekday: 1,
      currentTimestamp: Math.round(new Date().getTime() / 1000),
      from_place: "TA",
      to_place: "DKU",

      enableCountdown: false,
      remainTimeString: "N/A",
      nearestTimestamp: 0,

      show_weekday_A: "none",
      show_weekday_B: "none",
      show_weekend_A: "none",
      show_weekend_B: "none",
    };
  },
  name: "App",
  components: {},
  mounted() {
    // this.current_time = new Date().getHours() + ":" + new Date().getMinutes();
    this.getCurrentWeekday();
    // console.log("from_place", this.from_place);
    // console.log("current_weekday", this.current_weekday);
    // console.log("currentTimestamp", this.currentTimestamp);
    this.dropdownOnChange();
    this.getNearestBusEveryTwoMins();
    this.refreshTime();
  },
  methods: {
    getNearestBusEveryTwoMins() {
      setInterval(() => {
        this.getNearestBus();
        this.getCurrentWeekday();
      }, 1000 * 60 * 2);
      // }, 1000 * 5);
    },

    getCurrentWeekday() {
      this.current_weekday = new Date().getDay();
    },

    refreshTime() {
      setInterval(() => {
        this.currentTimestamp = Math.round(new Date().getTime() / 1000);
        let timeDiff = this.nearestTimestamp - this.currentTimestamp;
        let remainMins = Math.floor(timeDiff / 60);
        let remainSecs = timeDiff - remainMins * 60;
        let remainMinsString;
        let remainSecsString;
        if (remainMins < 10) {
          remainMinsString = "0" + remainMins;
        } else {
          remainMinsString = remainMins;
        }
        if (remainSecs < 10) {
          remainSecsString = "0" + remainSecs;
        } else {
          remainSecsString = remainSecs;
        }
        if (this.enableCountdown) {
          this.remainTimeString = remainMinsString + ":" + remainSecsString;
        }

      }, 1000);
    },

    getNearestBus() {
      let timeList = [];
      if (this.current_weekday in shuttle_data["weekday_define"]) {
        // weekday
        if (this.from_place == shuttle_data["weekday_stops_A"][0]) {
          this.shuttle_data["weekday_A"].forEach(function (item) {
            timeList.push(item[0]);
          });
        } else if (this.from_place == shuttle_data["weekday_stops_B"][0]) {
          this.shuttle_data["weekday_B"].forEach(function (item) {
            timeList.push(item[0]);
          });
        }
      } else {
        // weekend
        if (this.from_place == shuttle_data["weekend_stops_A"][0]) {
          this.shuttle_data["weekend_A"].forEach(function (item) {
            timeList.push(item[0]);
          });
        } else if (this.from_place == shuttle_data["weekend_stops_B"][0]) {
          this.shuttle_data["weekend_B"].forEach(function (item) {
            timeList.push(item[0]);
          });
        }
      }
      // change to UNIX timestamps, and get the nearest one
      // let that = this;
      let nowTime = new Date(this.currentTimestamp * 1000);
      // console.log("nowTime", nowTime);
      // console.log("timeList", timeList)
      for (let i in timeList) {
        let item = timeList[i];
        // console.log("timeDiff", timeDiff)
        // console.log("item: ", item)
        let itemTime = new Date(
          nowTime.getFullYear(),
          nowTime.getMonth(),
          nowTime.getDate(),
          item.split(":")[0],
          item.split(":")[1],
          0
        );
        let timeDiff = itemTime.getTime() - nowTime.getTime();
        if (timeDiff > 0 && timeDiff < 60 * 60 * 1000) {
          this.nearestTimestamp = itemTime.getTime() / 1000;
          this.enableCountdown = true
          break;
        }
        this.enableCountdown = false;
        this.remainTimeString = ">1hr";
      }
    },

    dropdownOnChange() {
      if (this.from_place == "TA") {
        this.to_place = "DKU";
        this.enableCountdown = true;
      }
      if (this.from_place == "DKU") {
        this.to_place = "TA";
        this.enableCountdown = true;
      }
      if (this.from_place == "Lanting") {
        this.enableCountdown = false;
        this.remainTimeString = "N/A";
      }

      // console.log("from_place", this.from_place)
      // console.log("to_place", this.to_place)

      if (this.current_weekday in shuttle_data["weekday_define"]) {
        // weekday
        if (this.from_place == shuttle_data["weekday_stops_A"][1]) {
          this.show_weekday_A = "table";
          this.show_weekday_B = "table";
          this.show_weekend_A = "none";
          this.show_weekend_B = "none";
        }
        if (this.from_place == shuttle_data["weekday_stops_A"][0]) {
          this.show_weekday_A = "table";
          this.show_weekday_B = "none";
          this.show_weekend_A = "none";
          this.show_weekend_B = "none";
        }
        if (this.from_place == shuttle_data["weekday_stops_B"][0]) {
          this.show_weekday_A = "none";
          this.show_weekday_B = "table";
          this.show_weekend_A = "none";
          this.show_weekend_B = "none";
        }
      } else {
        // weekend
        if (this.from_place == shuttle_data["weekend_stops_A"][1]) {
          this.show_weekday_A = "none";
          this.show_weekday_B = "none";
          this.show_weekend_A = "table";
          this.show_weekend_B = "table";
        }

        if (this.from_place == shuttle_data["weekend_stops_A"][0]) {
          this.show_weekday_A = "none";
          this.show_weekday_B = "none";
          this.show_weekend_A = "table";
          this.show_weekend_B = "none";
        }
        if (this.from_place == shuttle_data["weekend_stops_B"][0]) {
          this.show_weekday_A = "none";
          this.show_weekday_B = "none";
          this.show_weekend_A = "none";
          this.show_weekend_B = "table";
        }
      }
      this.getNearestBus();
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Comfortaa:wght@600&display=swap");

#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  /* color: #2c3e50; */
  /* margin-top: 60px; */
}

* {
  font-size: 8px;
  outline: none;
}

hr {
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  margin: 1em 0;
}

body {
  margin: 0;
  background-color: rgb(246, 246, 246);
  font-family: Montserrat, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.container {
  margin: 1.8rem;
  display: flex;
  flex-direction: column;
}

.container > div {
  margin: 0.5rem 0;
}

.card {
  font-family: "Comfortaa", cursive;
  color: white;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(196, 196, 196, 0.3);
  height: 10rem;
  border-radius: 2rem;
  display: flex;
  padding: 3rem 2rem;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background: linear-gradient(
    75deg,
    #f17c58,
    #e94584,
    #24aadb,
    #27dbb1,
    #ffdc18,
    #ff3706
  );
  background-size: 600% 100%;
  animation: gradient 16s linear infinite;
  animation-direction: alternate;
}
@keyframes gradient {
  0% {
    background-position: 0%;
  }
  100% {
    background-position: 100%;
  }
}

.description {
  font-size: 1.5rem;
  font-family: "Comfortaa", cursive;
  margin-right: auto;
}

.time {
  font-size: 9.5rem;
}

.refresh {
  font-size: 3rem;
  align-self: end;
  padding-right: 0.5rem;
}
.container > .twodropdowns {
  margin: 2rem 0;
  vertical-align: top;
}

.twodropdowns {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.dropdown {
  display: inline-block;
  position: relative;
  overflow: hidden;
  height: 3rem;
  width: 18rem;
  background: #f2f2f2;
  /* border: 1px solid; */
  border-color: white #f7f7f7 whitesmoke;
  /* border-radius: 3px; */
  border-radius: 0.5rem;
  background-image: -webkit-linear-gradient(
    top,
    transparent,
    rgba(0, 0, 0, 0.06)
  );
  background-image: -moz-linear-gradient(top, transparent, rgba(0, 0, 0, 0.06));
  background-image: -o-linear-gradient(top, transparent, rgba(0, 0, 0, 0.06));
  background-image: linear-gradient(
    to bottom,
    transparent,
    rgba(0, 0, 0, 0.06)
  );
  -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.08);
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.08);
}

.dropdown:before,
.dropdown:after {
  content: "";
  position: absolute;
  z-index: 2;
  top: 1.4rem;
  right: 10px;
  border: 3px dashed;
  border-color: #888888 transparent;
  pointer-events: none;
}

.dropdown:before {
  border-bottom-style: solid;
  border-top: none;
}

.dropdown:after {
  margin-top: 0.5rem;
  border-top-style: solid;
  border-bottom: none;
}

.dropdown-select {
  position: absolute;
  margin: auto;
  padding: 1rem;
  font-size: 1.3rem;
  color: #62717a;
  text-shadow: 0 1px white;
  background: #f2f2f2; /* Fallback for IE 8 */
  background-color: white;
  background: rgba(
    0,
    0,
    0,
    0
  ) !important; /* "transparent" doesn't work with Opera */
  border: 0;
  border-radius: 0;
  -webkit-appearance: none;
}

.dropdown-select:focus {
  z-index: 3;
  width: 100%;
  /* color: #394349; */
  /* outline: 2px solid #49aff2; */
  /* outline: 2px solid -webkit-focus-ring-color; */
  /* outline-offset: -2px; */
}

.dropdown-select > option {
  margin: 3px;
  padding: 6px 8px;
  text-shadow: none;
  background: #f2f2f2;
  border-radius: 3px;
  cursor: pointer;
}
.rwd-table {
  margin: 1em 0;
  padding: 1em 1.5em;
}
.rwd-table tr {
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
}
.rwd-table th {
  font-size: 2rem;
  display: none;
}
.rwd-table td {
  font-size: 1.5rem;
  display: block;
}

.rwd-table td:before {
  display: none;
}

.rwd-table th,
.rwd-table td {
  text-align: center;
}

.rwd-table th,
.rwd-table td {
  display: table-cell;
  padding: 0.25em 0.5em;
}
.rwd-table th:first-child,
.rwd-table td:first-child {
  padding-left: 0;
}
.rwd-table th:last-child,
.rwd-table td:last-child {
  padding-right: 0;
}

.rwd-table {
  background: #34495e;
  color: #fff;
  border-radius: 2em;
  overflow: hidden;
}
.rwd-table tr {
  border-color: #46637f;
}
.rwd-table th,
.rwd-table td {
  margin: 0.5em 1em;
}
@media (min-width: 480px) {
  .rwd-table th,
  .rwd-table td {
    padding: 1em !important;
  }
}
.rwd-table th,
.rwd-table td:before {
  color: #dd5;
}
</style>

