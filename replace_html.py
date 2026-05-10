from bs4 import BeautifulSoup

chinese_summaries = [
    """<ul>
  <li><strong>提出开源轻量级全向模型 MiniMind-O</strong>：报告了 MiniMind-O，这是一个原生支持语音的极轻量全向模型，仅有 30 亿（3B）参数，为资源受限环境提供了强大的多模态处理能力。</li>
  <li><strong>创新的多模态架构设计</strong>：该模型集成了针对视觉（Vision）、连续音频（Audio）和文本（Text）的多模态投影仪，并通过结合 DPO 和 RLHF 的自举强化学习，在基础预训练（支持中英文）之上进行了深度对齐。</li>
  <li><strong>突破端侧模型性能极限</strong>：在超过 11 个涵盖图像、视频理解以及文本/音频生成的多模态基准测试中，MiniMind-O 展现出比同规模模型甚至部分大型专有模型更优越的性能，并且所有权重均已开源。</li>
</ul>""",
    """<ul>
  <li><strong>提出多分辨率编解码器架构 MuCodec</strong>：提出了一种创新的具有多分辨率重采样架构的神经音频编解码器（MuCodec），旨在解决从高采样率音频中提取声学离散标记时由于时间分辨率过高而导致的语言模型处理效率低下的问题。</li>
  <li><strong>融合结构重参数化与多分辨率处理</strong>：通过应用结构重参数化技术，显著降低了音频解码过程中的延迟。同时，多分辨率设计使得低分辨率帧处理能有效避免在捕获宽感受野时时间维度的丢失，而高分辨率处理则专注于捕捉精细的时序细节以提升音频质量。</li>
  <li><strong>实现高质量、低延迟音频重建</strong>：主观与客观的评估结果显示，MuCodec 不仅提供了与基线模型相当的高水平重构质量，更在推理速度上实现了高达 3.7 倍的大幅提升，为高效的语音生成模型奠定了坚实基础。</li>
</ul>""",
    """<ul>
  <li><strong>提出基于文本的3D声环境生成框架 ControlRoom3D</strong>：提出了一个名为 ControlRoom3D 的扩散模型框架，专门用于在复杂条件下（如多向声音生成）根据文本提示生成和控制声学环境。</li>
  <li><strong>突破训练数据瓶颈</strong>：为了解决现实世界房间脉冲响应（RIR）数据有限的问题，该研究利用声学模拟器结合现有 3D 网格数据集的子集，高效合成了包含几何声学参数的训练数据，实现了在没有大规模真实数据集情况下的模型训练。</li>
  <li><strong>实现高精度的空间声学控制</strong>：在 DCASE 基准测试上的广泛实验表明，该方法能够克服现有技术的限制，不仅能处理复杂的空间文本查询，还能根据给定的文本描述高精度地合成空间（双声道）音频。</li>
</ul>""",
    """<ul>
  <li><strong>最优传输音频距离 (OTAD)</strong>: 提出使用基于Wasserstein 1-距离的最佳传输音频距离(OTAD)，以更好地捕捉音频信号复杂的低维流形特征，这不仅改进了对音频失真的感知，且对细微变换更具鲁棒性。</li>
  <li><strong>学习黎曼基度量</strong>: 为了提升OTAD对高维音频数据的适用性，引入了学习得到的参数化黎曼度量来优化基础成本函数，克服了欧几里得基度量未能反映音频数据底层几何结构的缺陷。</li>
  <li><strong>性能显著提升</strong>: 评估表明，带有学习黎曼基度量的OTAD在多种音频质量评估指标上优于传统音频距离，且显著提升了相关分数。</li>
</ul>""",
    """<ul>
  <li><strong>零样本跨语言语音克隆 X-Voice</strong>: 提出X-Voice模型，这是一个能够在零样本条件下合成30种语言高质量语音的多语言TTS系统，可准确保留目标说话人的独特语音特征，且只需一段几秒钟的任意语言参考音频。</li>
  <li><strong>无需人工标注训练</strong>: X-Voice的训练全程无需任何人类标注，而是利用Whisper模型进行自动数据标注和质量过滤。</li>
  <li><strong>出色的零样本跨语言能力</strong>: 客观和主观评估均表明，在零样本跨语言语音合成上，X-Voice不仅超越了现有的多语言TTS模型和开源的语音基础模型，还显著增强了支持的语言范围，极大地推动了跨语言TTS领域的发展。</li>
</ul>""",
    """<ul>
  <li><strong>从输入端缩小模态差距</strong>: 指出语音大模型（SLMs）的关键瓶颈在于“输入端”。为了解决这一问题，提出TextPro-SLM，使语音输入更接近具备韵律感知能力的文本输入，从而同时保留文本大模型的语义能力和学习副语言特征。</li>
  <li><strong>整合WhisperPro编码器</strong>: TextPro-SLM结合了WhisperPro统一语音编码器（能产生同步文本词元和韵律嵌入），并通过一个被训练以维持原始TLM语义能力同时学习副语言理解的LLM骨干来运作。</li>
  <li><strong>数据高效且性能卓越</strong>: 实验显示，仅使用约1000小时的音频训练数据，TextPro-SLM在3B和7B参数规模下均实现了主流SLM中最小的模态差距，并在副语言理解任务上表现出色，证明了从输入端缩小模态差距是有效且数据高效的。</li>
</ul>""",
    """<ul>
  <li><strong>联合神经定向滤波与漫射声提取 NDF+</strong>: 提出了NDF+模型，它将虚拟定向麦克风(VDM)的估计重构为两个耦合的子任务：去混响VDM重建和漫射声提取，从而实现了对定向滤波和漫射声的联合控制。</li>
  <li><strong>灵活控制漫射成分</strong>: NDF+的重构方案使其能在最终的重建VDM输出中操纵漫射成分，提供了在空间声音捕获中控制漫射声音的额外自由度。</li>
  <li><strong>性能一致且优越</strong>: 在混响环境下的评估显示，NDF+在这两个子任务上一致优于传统基线模型，同时保持了与原版单任务NDF模型相当的VDM重建质量，且在立体声录音应用中，它可通过调节提取的漫射成分来实现可控的通道间电平差异。</li>
</ul>""",
    """<ul>
  <li><strong>预测-生成漂移分解框架 SIPS</strong>: 提出了一个用于语音增强和分离的即插即用框架（SIPS）。该方法基于随机插值，将插值动态分解为特定任务的漂移和随机去噪两部分，从而将强预测器的估算直接结合进生成采样过程中。</li>
  <li><strong>纯净语音训练与退化无关性</strong>: 仅使用纯净语音训练评分模型，从而产生一种可跨多种附加退化任务复用的“退化无关”先验，既保持了数学严谨性，又确保了感知上的自然性。</li>
  <li><strong>显著的质量提升与通用性</strong>: SIPS是一个不依赖特定架构约束的通用框架。结合最近的SEMamba和FlexIO等预测器，它持续改善了语音增强与分离的感知质量，在语音分离上甚至获得了高达+1.0 NISQA的增益。</li>
</ul>""",
    """<ul>
  <li><strong>紧凑的联合表征 WavCube</strong>: 提出WavCube，这是一种源自自监督学习（SSL）语音编码器的高效连续潜变量，它能在显著压缩维度（8倍）的同时，统一支持语音的理解、重建和生成任务。</li>
  <li><strong>两阶段语义-声学联合训练</strong>: WavCube采用两阶段训练方案。第一阶段通过语义瓶颈过滤不兼容扩散生成的SSL冗余特征；第二阶段通过端到端重建注入声学细节，并辅以语义锚定损失，确保特征不偏离原始语义流形。</li>
  <li><strong>多任务全能且性能优异</strong>: 实验表明，WavCube有效解决了SSL特征用于生成建模的两大缺陷。它在SUPERB理解基准上逼近WavLM性能，重建质量达到现有声学表征水平，在零样本TTS中提供最先进性能及更快的收敛速度，并且在SUPERB-SG基准的增强、分离和转换任务中表现卓越。</li>
</ul>""",
    """<ul>
  <li><strong>为Transformer权重衰减提供泛函分析基础</strong>: 首次为大型语言模型中常用的结合L2正则化的交叉熵损失（权重衰减）提供了严格的泛函分析基础。证明了该正则化损失函数满足Villani强制能量函数标准（无限可微，至少二次增长，具有高斯可积尾部等）。</li>
  <li><strong>推导显式常数并验证</strong>: 从这种数学结构中推导出了显式的对数Sobolev和Poincaré常数，将正则化强度与模型维度与随机梯度下降的收敛保证及泛化界限联系起来。</li>
  <li><strong>理论预见与实验验证相符</strong>: 引入了一种可扩展的Villani诊断方法并进行了有效估计，在参数规模超1亿的GPT-Neo模型上通过实验证实了理论预测（包括Hessian矩阵的谱膨胀和与对数Sobolev分析一致的指数收敛行为），确立了深度学习中权重衰减的严格数学条件。</li>
</ul>""",
    """<ul>
  <li><strong>轻量级、非对称的多功能神经编解码器 LiVeAction</strong>: 提出了一种名为 LiVeAction 的轻量级、多功能且非对称的神经编解码器架构，专为资源受限的实时传感器和边缘计算设备设计，同时适用于传统和非传统信号模态。</li>
  <li><strong>FFT式结构与基于方差的率惩罚</strong>: 为了降低编码器复杂性，架构中施加了类似FFT的结构并减小了神经网络分析变换的深度与规模；同时，为了适应任意信号模态并简化训练，使用基于方差的速率惩罚取代了对抗性和感知损失。</li>
  <li><strong>优越的率失真性能与实用性</strong>: LiVeAction设计生成的编解码器不仅在率失真性能上优于最先进的生成式特征提取器（tokenizers），并且保持了在低功耗传感器上部署的极高实用性。</li>
</ul>""",
    """<ul>
  <li><strong>任务感知的答案保留式音频压缩</strong>: 深入研究了大音频语言模型（LALMs）部署中音频压缩对推理精度的影响。提出了“答案保留式音频压缩”的概念，强调以压缩引发的额外解答误差来评判压缩器，尤其关注那些受损最严重的特定查询类别。</li>
  <li><strong>压缩预算评估的验收协议</strong>: 建立了一个理论化的压缩器接受-拒绝标准，并推导出一种实用的验收协议（Sign-off Protocol），该协议具有统计置信度，能基于最坏情况测试给出安全的压缩预算。</li>
  <li><strong>揭示隐藏损伤与优化策略</strong>: 在五项音频问答基准测试上进行了验证，结果表明该协议成功暴露出在综合准确率掩盖下的类别级隐性损伤；研究进一步证明，合理的查询类别划分会改变可用的压缩预算，且基于特定查询的音频压缩策略有助于更好地保留答案精度。</li>
</ul>"""
]

file_path = "DEST_REPO/arxiv-daily/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
summaries = soup.find_all("div", class_="paper-summary")

if len(summaries) != 12:
    print(f"Error: Found {len(summaries)} summaries, expected 12.")
    exit(1)

for i, summary in enumerate(summaries):
    # clear contents
    summary.clear()
    # append parsed html bullet points
    parsed_ul = BeautifulSoup(chinese_summaries[i], "html.parser")
    summary.append(parsed_ul)

# Save the modified html keeping pretty formatting as much as possible
with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Successfully replaced summaries.")
