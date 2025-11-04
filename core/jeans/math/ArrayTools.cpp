// Array\Array.cpp

#include <Array\ArrayTools.h>
#include <Services\Log.h>
#include <math.h>


// Addition
// --------
template <class Type> void CArrayTools<Type>::Add(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc1;
	register Type*	l_pData3 = p_pSrc2;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	= *l_pData2++ + *l_pData3++;
}

template <class Type> void CArrayTools<Type>::Add(Type* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	+= *l_pData2++;
}

template <class Type> void CArrayTools<Type>::Add(Type* p_pDest, const Type p_Val, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	+= p_Val;
}

// Subtraction
// -----------
template <class Type> void CArrayTools<Type>::Sub(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc1;
	register Type*	l_pData3 = p_pSrc2;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	= *l_pData2++ - *l_pData3++;
}

template <class Type> void CArrayTools<Type>::Sub(Type* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	-= *l_pData2++;
}

template <class Type> void CArrayTools<Type>::Sub(Type* p_pDest, const Type p_Val, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	-= p_Val;
}

// Multiplication
// --------------
template <class Type> void CArrayTools<Type>::Mult(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc1;
	register Type*	l_pData3 = p_pSrc2;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	= *l_pData2++ * *l_pData3++;
}

template <class Type> void CArrayTools<Type>::Mult(Type* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	*= *l_pData2++;
}

template <class Type> void CArrayTools<Type>::Mult(Type* p_pDest, const Type p_Val, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	*= p_Val;
}

// Division
// ---------
template <class Type> void CArrayTools<Type>::Div(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc1;
	register Type*	l_pData3 = p_pSrc2;
	register int	l_dim = p_DimData;

	while(l_dim--)
	{	if(*l_pData3)
			(*l_pData1)	= (*l_pData2) / (*l_pData3);

		l_pData1++;
		l_pData2++;
		l_pData3++;
	}
}

template <class Type> void CArrayTools<Type>::Div(Type* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register Type*	l_pData1 = p_pDest;
	register Type*	l_pData2 = p_pSrc;
	register int	l_dim = p_DimData;

	while(l_dim--)
	{	if(*l_pData2)
			(*l_pData1)	/= (*l_pData2);

		l_pData1++;
		l_pData2++;
	}
}

template <class Type> void CArrayTools<Type>::Div(Type* p_pDest, const Type p_Val, const int p_DimData)
{
	if(p_Val == Type(0))
		return;

	register Type*	l_pData1 = p_pDest;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pData1++	/= p_Val;
}

// Absolute value
// --------------
template <class Type> void CArrayTools<Type>::Abs(Type* p_pDest, const int p_DimData)
{
	register Type*	l_pData = p_pDest;
	register int	l_Dim = p_DimData;
			 Type	l_Val;

	while(l_Dim--)
	{	l_Val		= *l_pData;
		*l_pData++	= Type(fabs(l_Val));
	}
}

// Square root
// -----------
template <class Type> void CArrayTools<Type>::Sqrt(Type* p_pDest, const int p_DimData, const Type p_IfLessZero)
{
	register Type*	l_pData = p_pDest;
	register int	l_Dim = p_DimData;
			 Type	l_Val;

	while(l_Dim--)
	{	l_Val		= *l_pData;
		*l_pData++	= (l_Val > 0) ? Type(sqrt(l_Val)) : p_IfLessZero;
	}
}

// Base 10 logarithm
// ------------------
template <class Type> void CArrayTools<Type>::Log10(Type* p_pDest, const int p_DimData, const Type p_IfLessOrEqZero)
{
	register Type*	l_pData = p_pDest;
	register int	l_Dim = p_DimData;
			 Type	l_Val;

	while(l_Dim--)
	{	l_Val			= *l_pData;
		*l_pData++	= (l_Val > 0) ? Type(log10(l_Val)) : p_IfLessOrEqZero;
	}
}

// Various value informations
// --------------------------
template <class Type> Type CArrayTools<Type>::GetMin(Type* p_pSrc, const int p_DimData, const BOOL p_NoZero)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	if(p_NoZero == TRUE)
	{	while(l_dim && (*l_pData == Type(0)))
		{	l_dim--;
			l_pData++;
		}

		if(l_dim)
			l_val = *l_pData;

		while(l_dim--)
		{	l_v = *l_pData;
			if(l_v && (l_v < l_val))
				l_val = l_v;
			l_pData++;
	}	}
	else
	{	l_val = *l_pData;
		while(l_dim--)
		{	l_v = *l_pData;
			if(l_v < l_val)
				l_val = l_v;
			l_pData++;
	}	}

	return l_val;
}

template <class Type> Type CArrayTools<Type>::GetMin(const int p_Incr, Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	l_val = *l_pData;
	while(l_dim>0)
	{	l_v = *l_pData;
		if(l_v < l_val)
			l_val = l_v;
		l_pData += p_Incr;
		l_dim--;
	}

	return l_val;
}

template <class Type> Type CArrayTools<Type>::GetMinPos(Type* p_pSrc, const int p_DimData, int& p_Pos)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	l_val = *l_pData;
	p_Pos	= 0;
	while(l_dim)
	{	l_v = *l_pData;
		if(l_v < l_val)
		{	l_val = l_v;
			p_Pos	= p_DimData - l_dim;
		}
		l_pData++;
		l_dim--;
	}

	return l_val;
}

template <class Type> Type CArrayTools<Type>::GetMax(Type* p_pSrc, const int p_DimData, const BOOL p_NoZero)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	if(p_NoZero == TRUE)
	{	while(l_dim && (*l_pData == Type(0)))
		{	l_dim--;
			l_pData++;
		}

		if(l_dim)
			l_val = *l_pData;

		while(l_dim--)
		{	l_v = *l_pData;
			if(l_v && (l_v > l_val))
				l_val = l_v;
			l_pData++;
	}	}
	else
	{	l_val = *l_pData;
		while(l_dim--)
		{	l_v = *l_pData;
			if(l_v > l_val)
				l_val = l_v;
			l_pData++;
	}	}

	return l_val;
}

template <class Type> Type CArrayTools<Type>::GetMax(const int p_Incr, Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	l_val = *l_pData;
	while(l_dim>0)
	{	l_v = *l_pData;
		if(l_v > l_val)
			l_val = l_v;
		l_pData += p_Incr;
		l_dim--;
	}

	return l_val;
}

template <class Type> Type CArrayTools<Type>::GetMaxPos(Type* p_pSrc, const int p_DimData, int& p_Pos)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				Type	l_val = 0, l_v;

	l_val = *l_pData;
	p_Pos	= 0;
	while(l_dim)
	{	l_v = *l_pData;
		if(l_v > l_val)
		{	l_val = l_v;
			p_Pos	= p_DimData - l_dim;
		}
		l_pData++;
		l_dim--;
	}

	return l_val;
}

template <class Type> double CArrayTools<Type>::GetSum(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				double	l_val = 0;

	while(l_dim--)
	{	l_val += *l_pData++;
	}

	return l_val;
}

template <class Type> double CArrayTools<Type>::GetEnergy(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				double	l_val, l_en = 0;

	while(l_dim--)
	{	l_val  = *l_pData++;
		l_en	+= l_val*l_val;
	}

	return l_en;
}

template <class Type> double CArrayTools<Type>::GetEntropy(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
				double	l_val, l_en = 0;

	while(l_dim--)
	{	l_val  = *l_pData++;
		if(l_val > 0)
			l_en	-= l_val*log10(l_val);
	}

	return l_en;
}

template <class Type> double CArrayTools<Type>::GetHomogeneity(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_ii = 0;
				double	l_en = 0;

	while(l_ii < p_DimData)
	{	l_en  += double(*l_pData++)/(1 + l_ii*l_ii);
		l_ii++;
	}

	return l_en;
}

template <class Type> double CArrayTools<Type>::GetInertia(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_ii = 0;
				double	l_en = 0;

	while(l_ii < p_DimData)
	{	l_en  += double(*l_pData++)*(l_ii*l_ii);
		l_ii++;
	}

	return l_en;
}

// various data processing operations
// ----------------------------------
template <class Type> void CArrayTools<Type>::Threshold(Type* p_pSrc, const int p_DimData, const Type p_Threshold, const ThreshModeEnum p_Mode)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
	
	switch(p_Mode)
	{	case LT:
			while(l_dim--)
			{	if(*l_pData < p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		case LEQ:
			while(l_dim--)
			{	if(*l_pData <= p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		case EQ:
			while(l_dim--)
			{	if(*l_pData == p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		case NEQ:
			while(l_dim--)
			{	if(*l_pData != p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		case GT:
			while(l_dim--)
			{	if(*l_pData > p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		case GEQ:
			while(l_dim--)
			{	if(*l_pData >= p_Threshold)
					*l_pData = 0;
				l_pData++;
			}
			break;
		default:
			ASSERT(FALSE);
			break;
	}
}

template <class Type> void CArrayTools<Type>::Binarize(Type* p_pSrc, const int p_DimData, const Type p_Threshold, const ThreshModeEnum p_Mode)
{
	register	Type*	l_pData = p_pSrc;
	register	int		l_dim = p_DimData;
	
	switch(p_Mode)
	{	case LT:
			while(l_dim--)
			{	*l_pData = Type(*l_pData < p_Threshold);
				l_pData++;
			}
			break;
		case LEQ:
			while(l_dim--)
			{	*l_pData = Type(*l_pData <= p_Threshold);
				l_pData++;
			}
			break;
		case EQ:
			while(l_dim--)
			{	*l_pData = Type(*l_pData == p_Threshold);
				l_pData++;
			}
			break;
		case NEQ:
			while(l_dim--)
			{	*l_pData = Type(*l_pData != p_Threshold);
				l_pData++;
			}
			break;
		case GT:
			while(l_dim--)
			{	*l_pData = Type(*l_pData > p_Threshold);
				l_pData++;
			}
			break;
		case GEQ:
			while(l_dim--)
			{	*l_pData = Type(*l_pData >= p_Threshold);
				l_pData++;
			}
			break;
		default:
			ASSERT(FALSE);
			break;
	}
}

template <class Type> void CArrayTools<Type>::GetMask(BYTE* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	BYTE*	l_pDataD = p_pDest;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
		*l_pDataD++ = *l_pDataS++ != 0;
}

template <class Type> void CArrayTools<Type>::Or(Type* p_pSrc, BYTE* p_pMask, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	BYTE*	l_pDataD = p_pMask;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
	{	*l_pDataS = Type((*l_pDataS != 0) | (*l_pDataD++ != 0));
		l_pDataS++;
	}
}

template <class Type> void CArrayTools<Type>::And(Type* p_pSrc, BYTE* p_pMask, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	BYTE*	l_pDataD = p_pMask;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
	{	*l_pDataS = Type((*l_pDataS != 0) & (*l_pDataD++ != 0));
		l_pDataS++;
	}
}

template <class Type> void CArrayTools<Type>::Xor(Type* p_pSrc, BYTE* p_pMask, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	BYTE*	l_pDataD = p_pMask;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
	{	*l_pDataS = Type((*l_pDataS != 0) ^ (*l_pDataD++ != 0));
		l_pDataS++;
	}
}

template <class Type> void CArrayTools<Type>::Not(Type* p_pSrc, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
	{	*l_pDataS = Type(!(*l_pDataS != 0));
		l_pDataS++;
	}
}

template <class Type> void CArrayTools<Type>::Mask(Type* p_pSrc, BYTE* p_pMask, const int p_DimData)
{
	register	Type*	l_pDataS = p_pSrc;
	register	BYTE*	l_pDataD = p_pMask;
	register	int		l_dim = p_DimData;
	
	while(l_dim--)
	{	if(*l_pDataD++ == 0)
			*l_pDataS = 0;
		l_pDataS++;
	}
}

template <class Type> void CArrayTools<Type>::GetHistogram(UINT* p_pDest, Type* p_pSrc, const int p_DimData)
{
	register	int		l_dim = p_DimData;
				UINT	l_val;
	
	while(l_dim--)
	{	l_val	= UINT(*p_pSrc++);
		(*(p_pDest+l_val))++;
	}
}

template <class Type> BOOL CArrayTools<Type>::GetStatistics(Type* p_pSrc, const int p_DimData,
	double& p_XMean, double& p_X2Mean, double& p_XVariance, const BOOL p_NoZero)
{
	register	Type*	l_pDataS = p_pSrc;
	register	int		l_dim = p_DimData;
				double	l_x=0, l_x2=0, l_val;
				int		l_nbElem = p_NoZero ? 0 : p_DimData;
	
	if(p_NoZero == TRUE)
	{	while(l_dim--)
		{	if(l_val	= double(*p_pSrc++) == Type(0))
				continue;

			l_nbElem++;
			l_x		+= l_val;
			l_x2	+= l_val*l_val;
	}	}
	else
	{	while(l_dim--)
		{	l_val	 = double(*p_pSrc++);
			l_x		+= l_val;
			l_x2	+= l_val*l_val;
	}	}

	if(l_nbElem == 0)
	{	p_XMean		= 0;
		p_X2Mean	= 0;
		p_XVariance	= 0;
		LOGMSG("Try to compute statisctics on an empty array");
		return FALSE;
	}

	p_XMean		= l_x/l_nbElem;	
	p_X2Mean	= l_x2/l_nbElem;	
	p_XVariance	= p_X2Mean - p_XMean*p_XMean;
	
	return TRUE;
}

template <class Type> double CArrayTools<Type>::GetCorrelation(Type* p_pSrc1, Type* p_pSrc2, const int p_DimData)
{
	register	Type*	l_pSrc1 = p_pSrc1;
	register	Type*	l_pSrc2 = p_pSrc2;
	register	int		l_dim = p_DimData;
	
	double	l_x1=0, l_x2=0, l_x1_2=0, l_x2_2=0, l_xy=0, l_v1, l_v2;
	while(l_dim--)
	{	l_v1	 = double(*l_pSrc1++);
		l_v2	 = double(*l_pSrc2++);

		l_x1	+= l_v1;
		l_x2	+= l_v2;
		l_x1_2	+= l_v1*l_v1;
		l_x2_2	+= l_v2*l_v2;
		l_xy	+= l_v1*l_v2;
	}

	double	l_m1 = l_x1/p_DimData;
	double	l_m2 = l_x2/p_DimData;
	double	l_s1 = sqrt(l_x1_2/p_DimData - l_m1*l_m1);
	double	l_s2 = sqrt(l_x2_2/p_DimData - l_m2*l_m2);
	double	l_cv = l_xy/p_DimData - l_m1*l_m2;
	
	return ((l_s1 > 0.000001) && (l_s2 > 0.000001)) ? l_cv/(l_s1*l_s2) : 0;
}

template <class Type> void CArrayTools<Type>::Qsort(Type* p_pSrc, const int p_DimData, const BOOL p_bAscending)
{
	if(p_bAscending == TRUE)	
		QsortAscending(p_pSrc, 0, p_DimData);
	else
		QsortDescending(p_pSrc, 0, p_DimData);
}

template <class Type> void CArrayTools<Type>::QsortAscending(Type* p_pData, int p_Low, int p_High)
{
	register int	ii, jj;
	BOOL			l_cnt = TRUE;

	while(l_cnt)
	{	l_cnt	= FALSE;
	
		for(ii=p_Low; ii < p_High; ii++)
		{	for(jj=ii+1; jj < p_High; jj++)
			{	if(p_pData[ii] > p_pData[jj])
				{	MSWAP(p_pData, ii, jj)
					l_cnt = TRUE;
	}	}	}	}
}

template <class Type> void CArrayTools<Type>::QsortDescending(Type* p_pData, int p_Low, int p_High)
{
	register int	ii, jj;
	BOOL			l_cnt = TRUE;

	while(l_cnt)
	{	l_cnt	= FALSE;
	
		for(ii=p_Low; ii < p_High; ii++)
		{	for(jj=ii+1; jj < p_High; jj++)
			{	if(p_pData[ii] < p_pData[jj])
				{	MSWAP(p_pData, ii, jj)
					l_cnt = TRUE;
	}	}	}	}
}

// Explicit instanciation for several types
// ----------------------------------------
template class CArrayTools<int>;
template class CArrayTools<short>;
template class CArrayTools<BYTE>;
template class CArrayTools<UINT>;
template class CArrayTools<long>;
template class CArrayTools<char>;
template class CArrayTools<WORD>;
template class CArrayTools<float>;
template class CArrayTools<double>;
template class CArrayTools<DWORD>;


// Type conversion
// ---------------
template <class TypeD, class TypeS> void Convert(TypeD* p_pDest, TypeS* p_pSrc, const int p_DimData)
{
	register TypeD*	l_pDataD = p_pDest;
	register TypeS*	l_pDataS = p_pSrc;
	register int	l_dim = p_DimData;

	while(l_dim--)
		*l_pDataD++ = TypeD(*l_pDataS++);
}

// Explicit instanciation for several types
// ----------------------------------------
template void Convert(int* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(int* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(short* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(short* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(BYTE* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(BYTE* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(UINT* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(UINT* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(long* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(long* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(char* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(char* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(WORD* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(WORD* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(float* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(float* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(double* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(double* p_pDest, DWORD* p_pSrc, const int p_DimData);

template void Convert(DWORD* p_pDest, int* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, short* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, BYTE* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, UINT* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, long* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, char* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, WORD* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, float* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, double* p_pSrc, const int p_DimData);
template void Convert(DWORD* p_pDest, DWORD* p_pSrc, const int p_DimData);

