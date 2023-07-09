document.addEventListener("DOMContentLoaded", function(){
    const banners = [
        {
            id: 1,
            image: "static/images/banner/b7.jpg",
            title: "SEASON SALE",
            subTitle: "Winter Collection -50% OFF",
        },
        {
            id: 2,
            image: "static/images/banner/b4.jpg",
            title: "NEW FOOTWEAR COLLECTION",
            subTitle: "Spring/Summer 2023",
        },
        {
            id: 3,
            image: "static/images/banner/b18.jpg",
            title: "T-Shirts",
            subTitle: "New Trendy Prints",
        },
    ]

    const bannerSection = document.getElementById('text-banner');
    let bannersContent = '';

    banners.forEach(banner => {
        const bannerContent = `
        <div class="banner-box">
                <h2>${banner.title}</h2>
                <h3>${banner.subTitle}</h3>
                <img src="${banner.image}" />
        </div>
    `;
    bannersContent += bannerContent;
    });

    if(bannerSection){
        bannerSection .innerHTML = bannersContent;
    }

})