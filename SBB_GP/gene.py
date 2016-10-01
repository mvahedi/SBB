###############################################################
###GENE OPERATORS
###############################################################

#MODE TARGET OPCODE SOURCE
#0 000 000 000
def encode(mode,target,opcode,source):
    target_greys = gcgen(TARGET_BIT_COUNT)
    op_greys = gcgen(OP_BIT_COUNT)
    source_greys = gcgen(SOURCE_BIT_COUNT);
    encoded_string = str(str(mode) + target_greys[target] + op_greys[opcode] + source_greys[source])
    return str(encoded_string)

def graycode(numbits, reverse = False):
    if numbits == 1:
        if reverse:
            yield "1"
            yield "0"
        else:
            yield "0"
            yield "1"
    else:
        if reverse:
            # all the "1"s start first
            gcprev = graycode(numbits - 1, True)
            for code in gcprev:
                yield "1" + code

            gcprev = graycode(numbits - 1, False)
            for code in gcprev:
                yield "0" + code
        else:
            # all the "0" start first
            gcprev = graycode(numbits - 1, False)
            for code in gcprev:
                yield "0" + code

            gcprev = graycode(numbits - 1, True)
            for code in gcprev:
                yield "1" + code

def gcgen(numbits = 2, reverse = False):
    i = 0
    greys = []
    for codes in graycode(numbits, reverse):
        greys.append(codes)
    return greys    

def decode(encoded):
    target_greys = gcgen(TARGET_BIT_COUNT)
    op_greys = gcgen(OP_BIT_COUNT)
    source_greys = gcgen(SOURCE_BIT_COUNT);
    #print 'decoding: ', encoded
    if len(encoded) <= OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT:
        mode = 0
        target = target_greys.index(str(encoded[0:TARGET_BIT_COUNT]))
        opcode = op_greys.index(str(encoded[TARGET_BIT_COUNT:TARGET_BIT_COUNT+OP_BIT_COUNT]))
        source = source_greys.index(str(encoded[TARGET_BIT_COUNT+OP_BIT_COUNT:]))
    else:
        mode = encoded[0]
        target = target_greys.index(str(encoded[1:TARGET_BIT_COUNT+1]))
        opcode = op_greys.index(str(encoded[TARGET_BIT_COUNT+1:TARGET_BIT_COUNT+OP_BIT_COUNT+1]))
        source = source_greys.index(str(encoded[TARGET_BIT_COUNT+OP_BIT_COUNT+1:]))
    return instruction(mode, target, opcode, source, encoded)