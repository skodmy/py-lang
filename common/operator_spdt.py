from xxxt.utils.common.spdtutils import TimeitDifferenceComputationModel


class OperatorTmtDiffCompMod(TimeitDifferenceComputationModel):
    setup4second = 'import operator'


op_model = OperatorTmtDiffCompMod()

op_model.comprint('2560 + 7540', 'operator.add(2560, 7540)')

op_model.comprint('7540 - 2560', 'operator.sub(7540, 2560)')

op_model.comprint('7540 * 2560', 'operator.mul(7540, 2560)')

op_model.comprint('7540 / 2560', 'operator.truediv(7540, 2560)')

op_model.second_statement = 'operator.pow(754, 2)'

op_model.comprint('754 * 754')

op_model.comprint('754 ** 2')

op_model.setup4first = 'import math'

op_model.comprint('math.pow(754, 2)')
