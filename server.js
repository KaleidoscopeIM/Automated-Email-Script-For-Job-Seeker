var cron = require('node-cron');

cron.schedule('0 8 * * *', () => {
    var spawn = require("child_process").spawn;
    var process = spawn('python', ["./sendMailRecruiter.py"]);
    //var process = spawn('python3', ["./sendMailRecruiter.py"]);
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    })
});