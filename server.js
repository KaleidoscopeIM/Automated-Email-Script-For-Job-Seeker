var cron = require('node-cron');

//local
// cron.schedule('* * * * *', () => {
//     var spawn = require("child_process").spawn;
//     var process = spawn('python', ["./sendMailRecruiter.py"]);
//     process.stdout.on('data', function(data) {
//         console.log(data.toString());
//     })
// });


//server
cron.schedule('* * * * *', () => { // 9 local == 13 on server
    var spawn = require("child_process").spawn;
    var process = spawn('python3', ["./gitPull.py"]);
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    })
    var process1 = spawn('python3', ["./sendMailRecruiter.py"]);
    process1.stdout.on('data', function(data) {
        console.log(data.toString());
    })
});