import { _decorator, Component, Node, Input, EventMouse, UITransform, Vec3, v3, instantiate, input, Vec2, EventKeyboard, KeyCode, Rect, Sprite, Color, builtinResMgr, resources, SpriteFrame, Layers, assetManager, Texture2D } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('BorderHighlight')
export class BorderHighlight extends Component {
    @property({ type: Node })
    public canvas: Node = null!; // 绑定Canvas节点
    private border: Node = null; // 边框预制体（需提前制作）
    private lastHitNode: Node = null; // 上一次点击的节点列表
    private isInUIMode: boolean = false; //是否可以点击高亮获取UI信息

    onLoad() {
        this.createBorder();
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }


    onDestroy() {
        // 销毁时移除监听
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }

    private createBorder(){
        this.border = new Node("Border");
        const borderTrans = this.border.addComponent(UITransform);
        this.border.setParent(this.canvas);
        this.border.setPosition(0, 0, 0);
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
            borderPart.setParent(this.border);
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
        if (event.keyCode != KeyCode.KEY_R) {
            return;
        }
        this.clearBorder();

        // 关闭
        if(this.isInUIMode){
            this.isInUIMode = false;
            this.setDefaultUIEvents(this.canvas, true);
            input.off(Input.EventType.MOUSE_DOWN, this.onMouseClick, this); 
            return;
        }

        // 打开
        this.isInUIMode = true;
        this.setDefaultUIEvents(this.canvas, false);
        input.on(Input.EventType.MOUSE_DOWN, this.onMouseClick, this); 
    }

    // 点击事件处理
    private onMouseClick(event: EventMouse) {
        // 获取点击位置（Vec2 转 Vec3）
        const screenPos = event.getLocation();
        const screenPosV3 = new Vec3(screenPos.x, screenPos.y, 0);
        console.log("点击", screenPos);
        
        // 转换为 Canvas 坐标系下的 Vec3
        const worldPos = this.canvas.getComponent(UITransform)!.convertToNodeSpaceAR(screenPosV3);
        const worldPosV2 = new Vec2(worldPos.x, worldPos.y);
        // 传递给 checkNodes 时保持 Vec3 类型
        const hitNodes: Node[] = [];
        this.checkNodes(this.canvas, worldPosV2, hitNodes);
    
        // 移除旧边框
        this.clearBorder();
    
        if (hitNodes.length == 0) {
            this.lastHitNode = null;
            return;
        } 
        // 判断是否同一位置点击
        let currentIndex = hitNodes.indexOf(this.lastHitNode) + 1;
        if(currentIndex >= hitNodes.length){
            currentIndex = 0;
        }

        // 保存当前节点列表
        this.lastHitNode = hitNodes[currentIndex];

        // 添加新边框
        this.addBorderToNode(this.lastHitNode);
        let elementData = `{"locator": "${this.lastHitNode.getPathInHierarchy()}"`;
        if(this.lastHitNode.getComponent(UITransform) != null){
            elementData += `, "focus": (${this.lastHitNode.getComponent(UITransform).anchorX}, ${this.lastHitNode.getComponent(UITransform).anchorY})`;
        }
        elementData += `}`;
        console.log(elementData);
        console.log("节点附带组件：",this.lastHitNode.components);

            
    }

    // 添加边框到指定节点
    private addBorderToNode(targetNode: Node) {
        // 改变边框位置
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
    }

    // 清除当前边框
    private clearBorder() {
        // 将四条边缩放归零
        this.border.getComponentsInChildren(UITransform).forEach(uiTransform =>{
            uiTransform.setContentSize(0, 0);
        })
    }


    // 递归检测节点
    private checkNodes(node: Node, clickedPos: Vec2, result: Node[]) {
        if (!node.active) return;
        const uiTransform = node.getComponent(UITransform);
        if (!uiTransform) return;
        node.children.forEach(child => {
            this.checkNodes(child, clickedPos, result); // 传递父节点坐标
        });
        if (node == this.canvas){
            return;
        }

        // 转换为节点在 Canvas 坐标系下的位置
        const worldPos = this.canvas.getComponent(UITransform).convertToNodeSpaceAR(node.worldPosition);
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

        // 递归禁用指定节点及其子节点的 UI 组件
    private setDefaultUIEvents(node: Node, enable: boolean) {
        // 禁用 Button
        const button = node.getComponent('cc.Button');
        if (button) {
            button.enabled = enable;
        }

        // 禁用 Slider
        const slider = node.getComponent('cc.Slider');
        if (slider) {
            slider.enabled = enable;
        }

        // 禁用 Toggle
        const toggle = node.getComponent('cc.Toggle');
        if (toggle) {
            toggle.enabled = enable;
        }

        // 禁用 Toggle
        const editBox = node.getComponent('cc.EditBox');
        if (editBox) {
            editBox.enabled = enable;
        }

        // 递归处理子节点
        node.children.forEach(child => {
            this.setDefaultUIEvents(child, enable);
        });
    }
}


