var cron = require('node-cron');

cron.schedule('* * * * *', () => {
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./sendMailRecruiter.py"]);
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    })
});



// cron.schedule('0 13 * * *', () => { // 9 local == 13 on server
//     var spawn = require("child_process").spawn;
//     var process = spawn('python3', ["./sendMailRecruiter.py"]);
//     process.stdout.on('data', function(data) {
//         console.log(data.toString());
//     })
// });