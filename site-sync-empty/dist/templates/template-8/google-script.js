// Google Apps Script để nhận dữ liệu từ form RSVP và lưu vào Google Sheets
// Hướng dẫn setup:
// 1. Mở Google Sheets của bạn: https://docs.google.com/spreadsheets/d/10D2WBNRVmSxfzMoUXEV2aKxGpnX2KfLv_JrDgItuwLw/edit
// 2. Click "Extensions" > "Apps Script"
// 3. Xóa code mẫu và paste đoạn code dưới đây vào
// 4. Click "Deploy" > "New deployment"
// 5. Chọn type: "Web app"
// 6. Execute as: "Me"
// 7. Who has access: "Anyone"
// 8. Click "Deploy" và copy URL
// 9. Paste URL vào file page2.js thay cho 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE'

function doPost(e) {
    try {
        // Parse dữ liệu từ request
        const data = JSON.parse(e.postData.contents);

        // Lấy sheet đầu tiên trong spreadsheet
        const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

        // Thêm timestamp
        const timestamp = new Date();

        // Thêm row mới với dữ liệu
        // Các cột: Họ tên | Lời nhắn | Bạn sẽ đến chứ? | Bạn tham dự cùng ai?
        sheet.appendRow([
            data.name,
            data.message,
            data.attendance,
            data.guestCount,
            timestamp
        ]);

        // Trả về success
        return ContentService
            .createTextOutput(JSON.stringify({ 'result': 'success', 'data': data }))
            .setMimeType(ContentService.MimeType.JSON);

    } catch (error) {
        // Trả về error
        return ContentService
            .createTextOutput(JSON.stringify({ 'result': 'error', 'error': error.toString() }))
            .setMimeType(ContentService.MimeType.JSON);
    }
}

// Function test (optional)
function doGet(e) {
    return ContentService.createTextOutput("Google Apps Script is running!");
}
