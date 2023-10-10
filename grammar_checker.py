import pgf
import pgfaux.analyze as an
import pgfaux.generate as gen
from results import GrammarResult as gr
from time import time

g = pgf.readPGF('ZMLargeExtChunk.pgf')
zul = g.languages['ZMLargeExtChunkZul']

MAX_TRIES = 3

QUAL_VPS = [
    ('CopAP',gr.QUAL_ADJ_AGREEMENT),
    ('CopNP',gr.QUAL_ID_NP_AGREEMENT),
    ('CopNPAssoc',gr.QUAL_ASSOC_NP_AGREEMENT),
    ('CopLocative',gr.QUAL_LOC_AGREEMENT),
    ('UseV',gr.QUAL_VERB_AGREEMENT),
    ('ComplV2',gr.QUAL_VERB_AGREEMENT),
    ('ComplVV',gr.QUAL_VERB_AGREEMENT),
    ('ComplVS',gr.QUAL_VERB_AGREEMENT)
]

SUBJ_VPS = [
    ('CopAP',gr.SUBJ_ADJ_AGREEMENT),
    ('CopNP',gr.SUBJ_ID_NP_AGREEMENT),
    ('CopNPAssoc',gr.SUBJ_ASSOC_NP_AGREEMENT),
    ('CopLocative',gr.SUBJ_LOC_AGREEMENT),
    ('UseV',gr.SUBJ_VERB_AGREEMENT),
    ('ComplV2',gr.SUBJ_VERB_AGREEMENT),
    ('ComplVV',gr.SUBJ_VERB_AGREEMENT),
    ('ComplVS',gr.SUBJ_VERB_AGREEMENT)
]

def get_first_parses(sentence: str,n=3):
    parses = []
    for i in range(n):
        try:
            i = zul.parse(sentence)
            _,e = next(i)
            parses.append(e)
        except StopIteration:
            break
    return parses

def get_first_child(chunk_expr):
    return an.children_trees(chunk_expr)[0]

def adjacent_chunks_of_cat(chunks: list,cat_list1: 'list[str]',cat_list2: 'list[str]'):
    for i in range(len(chunks)-1):
        if an.root_cat(chunks[i],g) in cat_list1 and an.root_cat(chunks[i+1],g) in cat_list2:
            return (chunks[i],chunks[i+1])

def _pred_check(np_pred_pair: tuple,fun: str,result: 'list[gr]'):
    pred_vps = an.subtrees_of_fun(np_pred_pair[1],fun)
    if len(pred_vps) > 0:
        np_lin = zul.linearize(np_pred_pair[0])
        s_lin = zul.linearize(np_pred_pair[1])
        lin = f'{np_lin} {s_lin}'
        return (result,lin)
    return None,''

def check_sentence(sentence: str):

    start_time = time()
    i = zul.parse(sentence)
    tries = 0
    while tries < MAX_TRIES:
        tries += 1
        try:
            prob,p = next(i)
        except:
            break

        if an.root_str(p) == 'PhrUtt': # sentence parsed as single unit
                return (gr.CORRECT,sentence,'')

        parsed_time = time()
        print('parsed: ',parsed_time - start_time)

        cs = an.subtrees_of_cat(p,'Chunk',g,False)
        cs_str = [str(c) for c in cs]
        print(cs_str)
        cs = [get_first_child(c) for c in cs]

        subtrees_analysed_time = time()
        print('analysed: ',subtrees_analysed_time - parsed_time)
        
        # qualificative agreement issue
        nps = ['Chunk_NP']
        ss = ['Chunk_RS']
        np_rs_pair = adjacent_chunks_of_cat(cs,nps,ss)
        if np_rs_pair:
            for (fun,error) in QUAL_VPS:
                result,bad_lin = _pred_check(np_rs_pair,fun,error)
                error_found_time = time()
                print('identified: ',error_found_time - subtrees_analysed_time)
                if result:
                    # extract largest possible NP from np chunk
                    np_id = an.cat_node_ids(np_rs_pair[0],'NP',g)[-1]
                    np_expr = an.subtree_at_id(np_rs_pair[0],np_id)
                    # extract RS from rs chunk
                    rs_id = an.cat_node_ids(np_rs_pair[1],'RS',g)[0]
                    rs_expr = an.subtree_at_id(np_rs_pair[1],rs_id)
                    # place into template to get good_lin
                    good_expr = pgf.Expr('RelNP',[np_expr,rs_expr])
                    good_lin = zul.linearize(good_expr)
                    replacement_found_time = time()
                    print('replaced: ',replacement_found_time - error_found_time)
                    return result,bad_lin,good_lin
        
        # subject-predicate agreement issue
        nps = ['Chunk_NP']
        ss = ['Chunk_S']
        np_s_pair = adjacent_chunks_of_cat(cs,nps,ss)
        if np_s_pair:
            for (fun,error) in SUBJ_VPS:
                result,bad_lin = _pred_check(np_s_pair,fun,error)
                error_found_time = time()
                print('identified: ',error_found_time - subtrees_analysed_time)
                if result:
                    # extract largest possible NP from np chunk
                    np_id = an.cat_node_ids(np_s_pair[0],'NP',g)[-1]
                    np_expr = an.subtree_at_id(np_s_pair[0],np_id)
                    # identify position of pron-based np in s
                    pron_np_id = an.fun_node_ids(np_s_pair[1],'UsePron')[0]
                    # place into sentence chunk to get good_lin
                    good_expr = gen.replace_at_id(np_s_pair[1],np_expr,pron_np_id)
                    good_lin = zul.linearize(good_expr)
                    replacement_found_time = time()
                    print('replaced: ',replacement_found_time - error_found_time)
                    return result,bad_lin,good_lin
        
    return (gr.NO_ERRORS_FOUND,sentence,'')
