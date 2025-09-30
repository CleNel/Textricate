let canvas = new fabric.Canvas('pdf-canvas');
let filename = "";
let currentPage = 0;
let totalPages = 1;
let bboxesPerPage = {};
let pdfWidth = 0;
let pdfHeight = 0;
let isDrawing = false;
let rect;

// -------------------- UPLOAD --------------------
document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("pdf-file");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    filename = fileInput.files[0].name;

    currentPage = 0;
    bboxesPerPage = {};

    await loadPage(currentPage, formData); // first load
});

// -------------------- EXTRACT --------------------
document.getElementById("extract-btn").addEventListener("click", async () => {
    const res = await fetch("/extract", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ filename, bboxes_per_page: bboxesPerPage })
    });
    const data = await res.json();
    document.getElementById("results").textContent = JSON.stringify(data.texts, null, 2);
});

// -------------------- CLEAR BOXES --------------------
document.getElementById("clear-boxes-btn").addEventListener("click", () => {
    canvas.getObjects().forEach(obj => { if(obj.type==='rect') canvas.remove(obj); });
    bboxesPerPage[currentPage] = [];
});

// -------------------- DRAWING --------------------
canvas.on('mouse:down', function(o){
    if(o.target && o.target.type === 'rect') return;

    isDrawing = true;
    let pointer = canvas.getPointer(o.e);

    rect = new fabric.Rect({
        left: pointer.x,
        top: pointer.y,
        width: 0,
        height: 0,
        fill: 'rgba(0,0,255,0.3)',
        stroke: 'blue',
        strokeWidth: 2,
        selectable: true
    });
    canvas.add(rect);
});

canvas.on('mouse:move', function(e){
    if(!isDrawing) return;
    let pointer = canvas.getPointer(e.e);
    rect.set({ width: pointer.x - rect.left, height: pointer.y - rect.top });
    canvas.renderAll();
});

canvas.on('mouse:up', function(){
    if(!isDrawing) return;
    isDrawing = false;

    let bbox = [rect.left, rect.top, rect.left + rect.width, rect.top + rect.height];

    if(!bboxesPerPage[currentPage]) bboxesPerPage[currentPage] = [];
    bboxesPerPage[currentPage].push(bbox);
});

// -------------------- LOAD PAGE --------------------
async function loadPage(pageNum, formData=null) {
    try {
        let url = `/upload?filename=${filename}&page=${pageNum}`;
        let response = formData ? await fetch(url, { method:"POST", body:formData }) : await fetch(url);
        const data = await response.json();
        if(data.error){ alert(data.error); return; }

        pdfWidth = data.page_width;
        pdfHeight = data.page_height;
        totalPages = data.total_pages;
        document.getElementById("page-number").innerText = `Page ${pageNum+1} / ${totalPages}`;

        canvas.clear();
        canvas.setWidth(pdfWidth);
        canvas.setHeight(pdfHeight);

        fabric.Image.fromURL(data.preview_url, function(img){
            img.set({ left:0, top:0, selectable:false, evented:false });
            canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        });

    } catch(err){
        console.error("Error loading page:", err);
    }
}

// -------------------- NAVIGATION --------------------
document.getElementById("prev-page").addEventListener("click", ()=>{
    if(currentPage>0){ currentPage--; loadPage(currentPage); }
});
document.getElementById("next-page").addEventListener("click", ()=>{
    if(currentPage<totalPages-1){ currentPage++; loadPage(currentPage); }
});
