import { _decorator, Component, Node, Input, EventMouse, UITransform, Vec3, input, Vec2, EventKeyboard, KeyCode, Rect, Sprite, Color, SpriteFrame, Layers, Texture2D, director, instantiate, find } from 'cc';
const { ccclass} = _decorator;

@ccclass('BorderHighlight')
export class BorderHighlight extends Component {
    private borderPrefab: Node = null; // 边框预制体（需提前制作）
    private border: Node = null;
    private lastHitNodes: Node[] = []; // 上一次点击的节点列表
    private lastHitNode: Node = null; // 上一次点击的节点
    private isInUIMode: boolean = false; //是否可以点击高亮获取UI信息
    private disabledMap: Map<Node, Component[]> = new Map();
    private disabledSet: Set<Node> = new Set();
    private canvasName: string = "ui_layer";

    onLoad() {
        director.addPersistRootNode(this.node);
        this.createBorderPrefab();
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }


    onDestroy() {
        // 销毁时移除监听
        this.quitUIMode();
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }

    update() {
        if(this.isInUIMode){
            this.setDefaultUIEvents(find(this.canvasName), false);
        }
        
    }

    private createBorderPrefab(){
        this.borderPrefab = new Node("BorderPrefab");
        // 标记为常驻根节点（必须为根节点）
        this.borderPrefab.setParent(this.node);
        const borderTrans = this.borderPrefab.addComponent(UITransform);
        borderTrans.setAnchorPoint(0.5, 0.5); // 中心锚点
        borderTrans.setContentSize(0, 0);

        const getBlankTexture = () =>{
            const texture = new Texture2D();
            texture.reset({
                width: 1,
                height: 1,
                format: Texture2D.PixelFormat.RGBA8888, // 使用 RGBA 格式
            });
            // 生成纯白像素数据（每个像素 RGBA=255,255,255,255）
            const pixelData = new Uint8Array(4);
            pixelData.fill(0xFF); // 全部填充 255

            // 写入像素数据
            texture.uploadData(pixelData);
            return texture;
        }

        const createBorderPart = (nodeName: string) => {
            const borderPart = new Node(nodeName);
            borderPart.layer = Layers.Enum.UI_2D;
            const borderPartTrans = borderPart.addComponent(UITransform);
            borderPart.setParent(this.borderPrefab);
            borderPart.setPosition(0, 0, 0);
            borderPartTrans.setAnchorPoint(0.5, 0.5); // 中心锚点
            const sprite = borderPart.addComponent(Sprite);
            const spriteFrame = new SpriteFrame();
            spriteFrame.texture = getBlankTexture();
            sprite.spriteFrame = spriteFrame;
            borderPartTrans.setContentSize(0, 0);
            sprite.color = Color.MAGENTA; //紫色
        };

        // 生成四个边框
        createBorderPart('TopBorder');
        createBorderPart('BottomBorder');
        createBorderPart('LeftBorder');
        createBorderPart('RightBorder');
    }



    private onKeyDown(event: EventKeyboard) {
        // 判断按下的是 R 键
        if (event.keyCode == KeyCode.KEY_R) {
                        // 关闭
            if(this.isInUIMode){
                this.quitUIMode();
                return;
            }
            this.enterUIMode();
            return;
        }

        // 切换选框
        if (event.keyCode == KeyCode.EQUAL){
            this.changeHitNode(1);
            return;
        }
        if (event.keyCode == KeyCode.DASH){
            this.changeHitNode(-1);
            return;
        }


    }

    private changeHitNode(dir: number){
        if(this.lastHitNodes.length == 0){
            return;
        }
        if(this.lastHitNode == null){
            return;
        }

        let currentIndex = this.lastHitNodes.indexOf(this.lastHitNode);
        if(currentIndex < 0){
            return;
        }
        // 移除旧边框
        this.clearBorder();
        currentIndex += dir;
        if(currentIndex >= this.lastHitNodes.length){
            currentIndex = 0;
        }
        else if(currentIndex < 0){
            currentIndex = this.lastHitNodes.length - 1;
        }
        this.lastHitNode = this.lastHitNodes[currentIndex];
        // 添加新边框
        this.addBorderToNode(this.lastHitNode);
    }

    private enterUIMode(){
        this.isInUIMode = true;
        this.setDefaultUIEvents(find(this.canvasName), false);
        input.on(Input.EventType.MOUSE_DOWN, this.onMouseClick, this);
    }

    private quitUIMode(){
        this.clearBorder();
        this.isInUIMode = false;
        this.setDefaultUIEvents(find(this.canvasName), true);
        input.off(Input.EventType.MOUSE_DOWN, this.onMouseClick, this);
    }

    private compareHitNodes(nodesA: Node[], nodesB: Node[]){

        if(nodesA.length != nodesB.length){
            return false;
        }
        let cur = 0;
        while(cur < nodesA.length){
            if(nodesA[cur].uuid != nodesB[cur].uuid){
                return false;
            }
            cur += 1;
        }
        return true;
    }

    // 点击事件处理
    private onMouseClick(event: EventMouse) {
        // 获取点击位置（Vec2 转 Vec3）
        const screenPos = event.getLocation();
        const screenPosV3 = new Vec3(screenPos.x, screenPos.y, 0);
        const canvas = find(this.canvasName);
        // 转换为 Canvas 坐标系下的 Vec3
        const worldPos = canvas.getComponent(UITransform)!.convertToNodeSpaceAR(screenPosV3);
        const worldPosV2 = new Vec2(worldPos.x, worldPos.y);
        // 传递给 checkNodes 时保持 Vec3 类型
        let hitNodes: Node[] = [];
        this.checkNodes(canvas, canvas, worldPosV2, hitNodes);
        hitNodes = this.sortNodesByArea(hitNodes);

        // 移除旧边框
        this.clearBorder();

        if (hitNodes.length == 0) {
            this.lastHitNode = null;
            this.lastHitNodes = hitNodes;
            return;
        }

        const isSamePosition = this.compareHitNodes(this.lastHitNodes, hitNodes);


        // 判断是否同一位置点击
        let currentIndex = hitNodes.indexOf(this.lastHitNode) + 1;
        if(!isSamePosition){
            currentIndex = 0;
        }
        
        if(currentIndex >= hitNodes.length){
            currentIndex = 0;
        }
        this.lastHitNodes = hitNodes;

        // 保存当前节点列表
        this.lastHitNode = hitNodes[currentIndex];

        // 添加新边框
        this.addBorderToNode(this.lastHitNode);
    }

    // 添加边框到指定节点
    private addBorderToNode(targetNode: Node) {
        // 改变边框位置
        this.border = instantiate(this.borderPrefab);
        this.border.setParent(targetNode.parent);
        // this.border.setPosition(0, 0, 0);
        const uiTransform = targetNode.getComponent(UITransform);
        const posX = targetNode.worldPosition.x + (0.5 - uiTransform.anchorX) * uiTransform.contentSize.x;
        const posY = targetNode.worldPosition.y + (0.5 - uiTransform.anchorY) * uiTransform.contentSize.y;
        const worldPosition = new Vec3(posX, posY, targetNode.worldPosition.z);
        this.border.setWorldPosition(worldPosition);

        // 调整边框尺寸与目标节点一致
        const width = uiTransform.width;
        const height = uiTransform.height;

        // 调整边框尺寸（比原尺寸稍大确保包裹）
        const borderSize = 4;  // 边框粗细
        const expand = 1;      // 扩展像素

        const updateBorderPart = (nodeName: string) => {
            const part = this.border.getChildByName(nodeName);
            if (!part){
                return;
            }

            const partTrans = part.getComponent(UITransform)!;
            switch(nodeName) {
                case 'TopBorder':
                    partTrans.setContentSize(width + expand*4, borderSize);
                    part.setPosition(0, height*0.5 + expand);
                    break;
                case 'BottomBorder':
                    partTrans.setContentSize(width + expand*4, borderSize);
                    part.setPosition(0, -height*0.5 - expand);
                    break;
                case 'LeftBorder':
                    partTrans.setContentSize(borderSize, height + expand*4);
                    part.setPosition(-width*0.5 - expand, 0);
                    break;
                case 'RightBorder':
                    partTrans.setContentSize(borderSize, height + expand*4);
                    part.setPosition(width*0.5 + expand, 0);
                    break;
            }
        };

        updateBorderPart('TopBorder');
        updateBorderPart('BottomBorder');
        updateBorderPart('LeftBorder');
        updateBorderPart('RightBorder');

        let elementData = `{"locator": "${this.lastHitNode.getPathInHierarchy()}"`;
        if(this.lastHitNode.getComponent(UITransform) != null){
            elementData += `, "focus": (${this.lastHitNode.getComponent(UITransform).anchorX}, ${this.lastHitNode.getComponent(UITransform).anchorY})`;
        }
        elementData += `}`;
        console.log(elementData,"\n",this.lastHitNode.components);
    }

    // 清除当前边框
    private clearBorder() {
        if (this.border) {
            this.border.destroy();
        }
        this.border = null;
    }

    private sortNodesByArea(nodes: Node[]): Node[] {
        // 过滤有效节点并计算面积
        const validNodes = nodes
            .filter(node => node.getComponent(UITransform))
            .map(node => ({
                node,
                area: node.getComponent(UITransform)!.contentSize.width *
                      node.getComponent(UITransform)!.contentSize.height
            }));

        // 按面积降序排序
        validNodes.sort((a, b) => a.area - b.area);

        // 返回排序后的节点数组
        return validNodes.map(item => item.node);
    }

    // 递归检测节点
    private checkNodes(node: Node, canvas: Node, clickedPos: Vec2, result: Node[]) {
        if (!node.activeInHierarchy && !this.disabledSet.has(node)) {
            return;
        }
        node.children.forEach(child => {
            this.checkNodes(child, canvas, clickedPos, result); // 传递父节点坐标
        });
        const uiTransform = node.getComponent(UITransform);
        if (!uiTransform) {
            return;
        }

        // 转换为节点在 Canvas 坐标系下的位置
        const worldPos = canvas.getComponent(UITransform).convertToNodeSpaceAR(node.worldPosition);
        const nodeX = worldPos.x - uiTransform.anchorX  * uiTransform.contentSize.width;
        const nodeY = worldPos.y - uiTransform.anchorY  * uiTransform.contentSize.height;

        // 按大小和位置生成Rect
        let rect = new Rect(nodeX, nodeY, uiTransform.contentSize.width, uiTransform.contentSize.height);

        // 判断点击是否在UI范围内
        if (!rect.contains(clickedPos)) {
            return;
        }
        result.push(node);
    }

    private updateDisableMap(node: Node, component: Component){
        component.enabled = false;
        const components = this.disabledMap.get(node);
        if(components==undefined){
            const components: Component[] = [component];
            this.disabledMap.set(node, components);
            return;
        }
        components.push(component);

    }

    // 递归禁用指定节点及其子节点的 UI 组件
    private setDefaultUIEvents(node: Node, enable: boolean) {
        if(node == null){
            return;
        }
        node.children.forEach(child => this.setDefaultUIEvents(child, enable));
        if (enable) {
            const components = this.disabledMap.get(node);
            if (components){
                components.forEach(c => c.enabled = true);
            }

            if(this.disabledSet.has(node)){
                node.active = true;
                this.disabledSet.delete(node);
            }
            return;
        }



        const componentsToDisable = [
            "cc.Button", "cc.Slider", "cc.Toggle", "cc.EditBox",
            "cc.PageView", "cc.ScrollView", "cc.VideoPlayer",
            "cc.WebView", "cc.BlockInputEvents"
        ];

        componentsToDisable.forEach(ComponentType => {
            const component = node.getComponent(ComponentType);
            if (component) {
                this.updateDisableMap(node, component);
            }
        });

        const nodeToDisable = ["_InputNode", "_ui_node_proxy"]
        nodeToDisable.forEach(nodeName => {
            if(nodeName == node.name){
                node.active = false;
                this.disabledSet.add(node);
            }
        })

    }
}


