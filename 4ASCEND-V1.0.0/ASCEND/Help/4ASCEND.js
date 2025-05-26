const pages = [
    {
        title: "游戏概要-1",
        image: "ascend.png",
        content: {
            template: "{{0}}是一款基于经典五子棋改编的双人对战游戏。",
            highlights: [
                { text: "4ASCEND", color: "#4eefdd" }
            ]
        }
    },

    {
        title: "游戏概要-2",
        image: "chessboard.png",
        content: {
            template: "玩家与对手分别为执白子的{{0}}和执黑子的{{1}}。<br>游戏目标是在落子抓住优势位置的同时，抓住机会向对手{{2}}最终战胜对手。",
            highlights: [
                { text: "精灵阵营", color: "#5276b6" },
                { text: "魔族阵营", color: "#e05e78" },
                { text: "发动攻击", color: "#4eefdd" }
            ]
        }
    },

    {
        title: "操作规则-1",
        image: "remove.png",
        content: {
            template: "使用{{0}}或{{1}}方向键进行移动<br>使用{{2}}或{{3}}键进行确认<br>(字母按键无法使用请按下Shift键)",
            highlights: [
                { text: "W-A-S-D", color: "#5276b6" },
                { text: "↑ ↓ ← →", color: "#e05e78" },
                { text: "Z", color: "#4eefdd"},
                { text: "Enter", color: "#e1a3e1"}
            ]
        }
    },

    {
        title: "操作规则-2",
        image: "suspend.png",
        content: {
            template: "游戏中可使用{{0}}键进行暂停",
            highlights: [{text: "Escape", color: "#e1a3e1"}]
        }
    },

    {
        title: "基本规则-1",
        image: "chessboard.png",
        content: {
            template: "在己方的回合内，玩家可以在盘面上线条交叉形成的点位上，选择一处尚未落子的位置，放置一枚已方颜色的棋子。",
            highlights: []
        }
    },

    {
        title: "基本规则-2",
        image: "attack.png",
        content: {
            template: "在棋盘上纵向、横向或斜向有4枚或以上的棋子连成一线<br>就会被从棋盘上拿起、进入攻击态势。这就是{{0}}。",
            highlights: [{text: "ASCEND", color: "#4eefdd"}]
        }
    },

    {
        title: "进攻与防守-1",
        image: "defend.png",
        content: {
            template: "一方构建出{{0}}后轮到对手如果不做出应对<br>则会受到相当于棋子数量的伤害值<br>作为{{0}}使用的棋子不会回到棋盘上",
            highlights: [
                { text: "ASCEND", color: "#4eefdd" }
            ]
        }
    },

    {
        title: "进攻与防守-2",
        image: "defend.png",
        content: {
            template: "如果一方构建出{{0}}后，对手通过落子也构成一个{{0}}的话，就会根据互相的棋子数量进行抵消<br>例如，当你做出了一个4枚棋子的攻击，对手立即连出了一个5枚棋子的{{0}}的话:<br>你作为进攻方反而会在抵消结束后受到{{1}}点伤害",
            highlights: [
                { text: "ASCEND", color: "#4eefdd" },
                { text: "1", color: "#e05e78"}
            ]
        }
    },

    {
        title: "胜利条件",
        image: "win.png",
        content: {
            template: "当有一方的生命值为0，或者当棋盘上81个位置都已经落满棋子时，游戏结束<br>游戏结束时{{0}}的一方获胜<br>盘面占满时，{{1}}获胜",
            highlights: [
                { text: "生还", color: "#e05e78" },
                { text: "精灵阵营", color: "#5276b6" }
            ]
        }
    },

    {
        title: "进阶技巧-1",
        image: "plant.png",
        content: {
            template: "随着对局的进行，棋盘上会长出{{0}}<br>落在{{0}}上的棋子，在组成{{1}}时攻击力{{2}}点，这意味着在抵消阶段时可以多抵消{{3}}枚对手的棋子。<br>(需注意，这并不会改变这枚棋子造成的直接伤害)",
            highlights: [
                { text: "魔力植物", color: "#daf9b0" },
                { text: "ASCEND", color: "#4eefdd" },
                { text: "+1", color: "#e05e78"},
                { text: "1", color: "#e05e78" },
            ]
        }
    },

    {
        title: "进阶技巧-2",
        image: "back-attack.png",
        content: {
            template: "此外，在对手做出{{0}}后如果立即在组成{{0}}的棋子的位置上落子则可以形成{{1}}，使得相应位置对手的棋子无效<br>而且，如果对手落在{{2}}上的棋子因你的反击而失效，则你也会将这株{{2}}纳入囊中，从而在反击中获得额外的优势",
            highlights: [
                {text: "ASCEND", color: "#5276b6"},
                {text: "反击", color: "#e1a3e1"},
                {text: "魔力植物", color: "#daf9b0"}
            ]
        }
    },

    {
        title: "进阶技巧-3",
        image: "backup.png",
        content: {
            template: "如果在对手发动{{0}}时你无法立即发动{{2}}进行抵消防御使用反击未尝不是一种降低损失的方法<br>在无法用{{0}}应对的不利局面下，使用这种战术轻松地为自己至少减少{{1}}点伤害或许会在无意中成为扭转战局的关键",
            highlights: [
                { text: "ASCEND", color: "#4eefdd" },
                { text: "1" , color: "#e1a3e1" },
                { text: "反击", color: "#e05e78" },
            ]
        }
    },

    {
        title: "进阶技巧-4",
        image: "grow.png",
        content: {
            template: "每次{{0}}的结算后棋盘上都会生长{{1}}<br>(但如果连续进行ASCEND的话，土地会变贫瘠，从而延缓{{1}}的生长。)<br>如果你感到战况焦灼，不妨抱着杀敌一千、自损八百的觉悟，背水一战后或许就会有新的出路。",
            highlights: [
                { text: "ASCEND", color: "#5276b6" },
                { text: "魔力植物", color: "#daf9b0" },
            ]
        }
    }



];

let currentPage = 0;

function updatePage() {
    const pageData = pages[currentPage];
    const textContainer = document.querySelector(".text");

    // 清空容器
    textContainer.innerHTML = '';

    // 创建内容容器
    const contentEl = document.createElement("p");
    contentEl.className = "dynamic-content";

    // 处理模板内容
    let processedContent = pageData.content.template;

    // 替换所有占位符
    processedContent = processedContent.replace(/\{\{(\d+)\}\}/g, (match, index) => {
        const hl = pageData.content.highlights[index];
        return `<span class="hl-item" style="color: ${hl.color}">${hl.text}</span>`;
    });

    contentEl.innerHTML = processedContent;
    textContainer.appendChild(contentEl);

    // 更新其他元素
    document.getElementById("page-1").textContent = `${currentPage + 1}/${pages.length}: ${pageData.title}`;
    document.querySelector(".image img").src = pageData.image;
}


// 翻页控制
function prevPage() {
    currentPage = (currentPage - 1 + pages.length) % pages.length;
    updatePage();
}

function nextPage() {
    currentPage = (currentPage + 1) % pages.length;
    updatePage();
}

// 按钮事件绑定
document.querySelector(".btn-up").addEventListener("click", prevPage);
document.querySelector(".btn-down").addEventListener("click", nextPage);

// 键盘事件监听
document.addEventListener("keydown", (e) => {
    switch(e.key) {
        case "ArrowLeft":
            prevPage();
            break;
        case "ArrowRight":
            nextPage();
            break;
    }
});

updatePage();
