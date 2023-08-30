window.onload = function () {
    /*
        1.設定範圍樣式
        2.放第一張圖
        3.放五張圖
        4.移動第一張圖
        5.設定分頁樣式
        6.滑鼠移入 移動圖片
        7.分頁換色
        8.箭頭樣式
        9.箭頭點擊事件
            後一張
            前一張
        10.自動輪播
    */
    //console.log(slideImgs);
    //slideImgs.style.left = -800 + 'px';
    let slideImgs = document.getElementById('slideImgs');
    let index = 0;
    let slideMove = 0;
    let pages = document.querySelectorAll('.pages li')
    //console.log(pages);
    for (let i = 0; i < pages.length; i++) {
        //console.log(pages[i]);
        pages[i].num = i;
        pages[i].addEventListener('mouseenter', function () {
            //console.log('123');
            //slideImgs.style.left = -800  + 'px'
            let index = this.num;
            let slideMove = -800 * index;
            slideImgs.style.left = slideMove + 'px';
            for (let j = 0; j < pages.length; j++) {
                pages[j].style.backgroundColor = '';

            }
            pages[index].style.backgroundColor = 'white';

        })

    }
    //箭頭往右

    let slideNext = document.getElementById('slideNext');
    slideNext.addEventListener('click', function () {
        index++;
        if (index >= 5) {
            index = 0;
        }
        moveImg();
    })


    // let slideMove = -800 * index;
    // slideImgs.style.left = slideMove + 'px';
    // for (let j = 0; j < pages.length; j++) {
    //     pages[j].style.backgroundColor = '';

    // }
    // pages[index].style.backgroundColor = 'white';

    //箭頭往左
    let slidePrev = document.getElementById('slidePrev');
    slidePrev.addEventListener('click', function () {
        index--;
        if (index < 0) {
            index = 4;
        }
        moveImg();
    })

    //自動輪播
    setInterval(function () {
        index++;
        if (index >= 5) {
            index = 0;
        }
        moveImg();
    }, 2000)
    function moveImg() {
        let slideMove = -800 * index;
        slideImgs.style.left = slideMove + 'px';
        for (let j = 0; j < pages.length; j++) {
            pages[j].style.backgroundColor = '';

        }
        pages[index].style.backgroundColor = 'white';
    }

}