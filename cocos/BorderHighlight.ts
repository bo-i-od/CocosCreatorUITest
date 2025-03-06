import { _decorator, Component, Node, Input, EventMouse, UITransform, Vec3, v3, instantiate, input, Vec2, EventKeyboard, KeyCode } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('BorderHighlight')
export class BorderHighlight extends Component {
    @property({ type: Node })
    public canvas: Node = null!; // 绑定Canvas节点

    @property({ type: Node })
    public borderPrefab: Node = null!; // 边框预制体（需提前制作）

    private lastHitNode: Node = null; // 上一次点击的节点列表
    private currentBorder: Node | null = null; // 当前高亮边框
    private isInUIMode: boolean = false;

    onLoad() {
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }


    onDestroy() {
        // 销毁时移除监听
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
    }

    private onKeyDown(event: EventKeyboard) {
        // 判断按下的是 R 键
        if (event.keyCode != KeyCode.KEY_R) {
            return;
        }
        this.clearCurrentBorder();
        if(this.isInUIMode){
            this.isInUIMode = false;
            this.setDefaultUIEvents(this.canvas, true);
            input.off(Input.EventType.MOUSE_DOWN, this.onMouseClick, this); 
            return;
        }
        this.isInUIMode = true;
        this.setDefaultUIEvents(this.canvas, false);
        input.on(Input.EventType.MOUSE_DOWN, this.onMouseClick, this); 
    }

    // 点击事件处理
    private onMouseClick(event: EventMouse) {
        // 获取点击位置（Vec2 转 Vec3）
        const screenPos = event.getLocation();
        const screenPosV3 = new Vec3(screenPos.x, screenPos.y, 0);
        
        // 转换为 Canvas 坐标系下的 Vec3
        const worldPos = this.canvas.getComponent(UITransform)!.convertToNodeSpaceAR(screenPosV3);

        const worldPosV2 = new Vec2(worldPos.x, worldPos.y);
        // 传递给 checkNodes 时保持 Vec3 类型
        const hitNodes: Node[] = [];
        this.checkNodes(this.canvas, worldPosV2, hitNodes);
    
        // 移除旧边框
        this.clearCurrentBorder();
    
        if (hitNodes.length == 0) {
            this.lastHitNode = null;
            return;
        } 
        // 判断是否同一位置点击
        let currentIndex = hitNodes.indexOf(this.lastHitNode) + 1;
        if(currentIndex >= hitNodes.length)
            currentIndex = 0;


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
        if (this.borderPrefab) {
            // 实例化边框并挂载到目标节点
            const border = instantiate(this.borderPrefab);
            border.setParent(targetNode);
            border.setPosition(Vec3.ZERO);
            
            // 调整边框尺寸与目标节点一致
            const uiTransform = targetNode.getComponent(UITransform)!;
            border.getComponent(UITransform)!.setContentSize(uiTransform.width, uiTransform.height);
            
            this.currentBorder = border;
        }
    }

    // 清除当前边框
    private clearCurrentBorder() {
        if (this.currentBorder) {
            this.currentBorder.removeFromParent();
            this.currentBorder.destroy();
            this.currentBorder = null;
        }
    }



    // 递归检测节点
    private checkNodes(node: Node, pos: Vec2, result: Node[]) {
        if (!node.active) return;
        const uiTransform = node.getComponent(UITransform);
        if (!uiTransform) return;
        const rect = uiTransform.getBoundingBox();
    
        node.children.forEach(child => {
            this.checkNodes(child, pos, result); // 传递父节点坐标
        });
        if(node === this.canvas){
            return;
        }
        if (!rect.contains(pos)) {
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


