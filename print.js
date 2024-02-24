const printer = require('printer');

// Get a list of available printers
const printers = printer.getPrinters();

// Assuming you have at least one printer installed
if (printers.length > 0) {
    const printerName = printers[0].name; // Assuming we'll use the first printer found

    // Print a text file
    printer.printFile({
        filename: 'file.txt',
        printer: printerName,
        success: function(jobID) {
            console.log("Job sent to printer with ID:", jobID);
        },
        error: function(err) {
            console.error("Error occurred:", err);
        }
    });
} else {
    console.log("No printers found!");
}
