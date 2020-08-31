var cron = require('node-cron');
// this file has been included in .gitignore


//local
// cron.schedule('* * * * *', () => {
//     var spawn = require("child_process").spawn;
//     var process = spawn('python', ["./sendMailRecruiter.py", "LOCAL"]);
//     process.stdout.on('data', function(data) {
//         console.log(data.toString());
//     })
// });


//server
cron.schedule('0 13 * * *', () => { // 9 local == 13 on server
    var spawn = require("child_process").spawn;
    var process = spawn('python3', ["./sendMailRecruiter.py", "SERVER"]);
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    })
});


// var spawn = require("child_process").spawn;
// var process = spawn('python', ["./sendMailRecruiter.py", "LOCAL"]);
// process.stdout.on('data', function(data) {
//     console.log(data.toString());
// })