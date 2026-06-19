# Quick count of current L01 pages by section
import sys; sys.path.insert(0,'/home/user/data-analysis/ielts_ppts')
import ppt_utils as U
U.set_theme(U.RGBColor(0x0F,0x4C,0x5C), U.RGBColor(0x12,0xA5,0x94),
            U.RGBColor(0xE6,0xF3,0xF1), U.RGBColor(0x07,0x2B,0x34), '听力', 'IELTS Listening')
p = U.new_prs()
# Test: one lesson with EXACTLY 7-page PARTs
def add_7page_part(p, idx, title_cn, title_en, concepts, contents, examples):
    U.section(p, idx, title_cn, title_en)
    for c in concepts: U.concept(p, c[0], c[1], c[2])
    for c in contents: U.content(p, c[0], c[1])
    for e in examples: U.example(p, e[0], e[1], answer=e[2], tip=e[3])
add_7page_part(p, 1, '测试PART', 'Test',
    [('概念1','导语1',[('a','b'),('c','d')])],
    [('内容1',[('e','f')]),('内容2',[('g','h')]),('内容3',[('i','j')])],
    [('例1','题目1','答案1','技巧1'),('例2','题目2','答案2','技巧2')])
print('7-page PART =', len(p.slides), 'slides (should be 7)')
