var statusList = document.getElementsByName('XID')[0].options;
packets = [['Patient ID','Packet type','Visit Num','Status']];
for(i=6; i < statusList.length; i++){
    label = statusList[i].label.split(" ");
    csv = [label[3], label[6], label[10], label[19]];
    packets[i] = csv;}

var csvContent = "data:text/csv;charset=utf-8,";
packets.forEach(function(infoArray, index){

    dataString = infoArray.join(",");
    csvContent += index < packets.length ? dataString+ "\n" : dataString;
});

var encodedUri = encodeURI(csvContent);
window.open(encodedUri);
