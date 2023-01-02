$(document).ready(function () {
  const bp = document.getElementById("bp").getContext("2d");
  const heat_body = document.getElementById("heat_body").getContext("2d");
  const heart_rate = document.getElementById("heart_rate").getContext("2d");
  const oksi = document.getElementById("oksi").getContext("2d");

  const c_bp = new Chart(bp, {
    type: "line",
    data: {
      datasets: [{ label: "Blood Pressure",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  const c_heat_body = new Chart(heat_body, {
    type: "line",
    data: {
      datasets: [{ label: "Heat Body",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  const c_heart_rate = new Chart(heart_rate, {
    type: "line",
    data: {
      datasets: [{ label: "Heart Rate",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  const c_oksi = new Chart(oksi, {
    type: "line",
    data: {
      datasets: [{ label: "Oksigen",  }],
    },
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  function addData(label, data, myChart) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstData(myChart) {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();


  setInterval(function() {
    socket.emit('save_data', {
      data_heart: (Math.random()*100).toFixed(2),
      data_heat: (Math.random()*100).toFixed(2),
      data_oksi: (Math.random()*100).toFixed(2),
      data_ir: (Math.random()*100).toFixed(2)
    });
}, 1000);


  socket.on('connect', function() {
    socket.emit('bp');
    socket.emit('heat_body');
    socket.emit('heart_rate');
    socket.emit('oksi');
  });

  socket.on('tempel', function(msg){
    document.getElementById("save_data").innerHTML = msg.data
  })

  socket.on("resp_bp", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (c_bp.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(c_bp);
    }
    addData(msg.date, msg.value, c_bp);
  });

  socket.on("resp_heat_body", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (c_heat_body.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(c_heat_body);
    }

    addData(msg.date, msg.value*(-3), c_heat_body)
  });

  socket.on("resp_heart_rate", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (c_heart_rate.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(c_heart_rate);
    }

    addData(msg.date, msg.value*2, c_heart_rate)
  });

    socket.on("resp_oksi", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (c_oksi.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(c_oksi);
    }

    addData(msg.date, msg.value*(-4), c_oksi)
  });

});

