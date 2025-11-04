// Array\Array1.cpp

#include "Array1.h"
//#include "Array\ArrayTools.h"

// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CArray1<Type>::CArray1(const int p_Width /* = 0 */) :
		CContainer1<Type>(p_Width) {}

template <class Type> CArray1<Type>::CArray1(const Type* p_Src, const int p_Width) : 
		CContainer1<Type>(p_Src, p_Width) {}

template <class Type> CArray1<Type>::CArray1(const CArray1<Type>& p_Src) :
		CContainer1<Type>(p_Src) {} 

template <class Type> CArray1<Type>::CArray1(const CArray1<Type>& p_Src, const int p_Width) : 
		CContainer1<Type>(p_Src, p_Width) {} 

// desctructor
// -----------
template <class Type> CArray1<Type>::~CArray1() {}


// Addition operators
// ------------------
template <class Type> CArray1<Type> CArray1<Type>::operator+(const CArray1<Type>& p_Arr)
{
	CArray1<Type> l_res;
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Add(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to add arrays of different size");
		
	return l_res;
}

template <class Type> CArray1<Type> CArray1<Type>::operator+(const Type p_Val)
{
	CArray1<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Add(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator+=(const CArray1<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Add(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to add arrays of different size");
	
	return *this;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator+=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Add(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subtraction operators
// ---------------------
template <class Type> CArray1<Type> CArray1<Type>::operator-(const CArray1<Type>& p_Arr)
{
	CArray1<Type> l_res;
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Sub(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("cannot create result array");
	}
	else
		LOGERR("Try to subtract arrays of different size");

	return l_res;
}

template <class Type> CArray1<Type> CArray1<Type>::operator-(const Type p_Val)
{
	CArray1<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Sub(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator-=(const CArray1<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Sub(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to subtract arrays of different size");
	
	return *this;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator-=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Sub(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Multiplication operators
// ------------------------
template <class Type> CArray1<Type> CArray1<Type>::operator*(const CArray1<Type>& p_Arr)
{
	CArray1<Type> l_res(*this);
	
	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Mult(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to multiply arrays of different size");
		
	return l_res;
}

template <class Type> CArray1<Type> CArray1<Type>::operator*(const Type p_Val)
{
	CArray1<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Mult(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator*=(const CArray1<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Mult(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to multiply arrays of different size");

	return *this;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator*=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Mult(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subdivision operators
// ---------------------
template <class Type> CArray1<Type> CArray1<Type>::operator/(const CArray1<Type>& p_Arr)
{
	CArray1<Type> l_res;

	if(Sizeof() == p_Arr.Sizeof())
	{
		l_res = (*this);
		if(!!l_res)
			CArrayTools<Type>::Div(l_res.GetBuffer(), p_Arr.GetBuffer(), l_res.GetNbElements());
		else
			LOGERR("Cannot create result array");
	}
	else
		LOGERR("Try to subdivide arrays of different size");
		
	return l_res;
}

template <class Type> CArray1<Type> CArray1<Type>::operator/(const Type p_Val)
{
	CArray1<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Div(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator/=(const CArray1<Type>& p_Arr)
{
	if(Sizeof() == p_Arr.Sizeof())
	{
		if(!!(*this))
			CArrayTools<Type>::Div(GetBuffer(), p_Arr.GetBuffer(), GetNbElements());
		else
			LOGERR("object not allocated properly");
	}
	else
		LOGERR("Try to subdivide arrays of different size");
	
	return *this;
}

template <class Type> const CArray1<Type>& CArray1<Type>::operator/=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Div(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// various operations
// ------------------
template <class Type> void CArray1<Type>::Abs()											
{
	CArrayTools<Type>::Abs(GetBuffer(), GetNbElements());
}

template <class Type> void CArray1<Type>::Sqrt(const Type p_IfLessZero /* = 0 */)											
{
	CArrayTools<Type>::Sqrt(GetBuffer(), GetNbElements(), p_IfLessZero);
}

template <class Type> void CArray1<Type>::Log10(const Type p_IfLessOrEqZero /* = 0 */)											
{
	CArrayTools<Type>::Log10(GetBuffer(), GetNbElements(), p_IfLessOrEqZero);
}

// conversion between types
// ------------------------
template <class Type> void CArray1<Type>::Convert(CArray1<char>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<char>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<short>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<WORD>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<int>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<UINT>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<long>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<DWORD>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<float>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray1<Type>::Convert(CArray1<double>& p_Result) const
{
	if(p_Result.SetSize(m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// various value informations
// --------------------------
template <class Type> Type CArray1<Type>::GetMin(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMin(GetBuffer(), GetNbElements(), p_NoZero);
}

template <class Type> Type CArray1<Type>::GetMinPos(int& p_Pos) const
{
	return CArrayTools<Type>::GetMinPos(GetBuffer(), GetNbElements(), p_Pos);
}

template <class Type> Type CArray1<Type>::GetMax(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMax(GetBuffer(), GetNbElements(), p_NoZero);
}

template <class Type> Type CArray1<Type>::GetMaxPos(int& p_Pos) const
{
	return CArrayTools<Type>::GetMaxPos(GetBuffer(), GetNbElements(), p_Pos);
}

template <class Type> double CArray1<Type>::GetMean() const 
{ 
	return GetSum()/GetNbElements(); 
}

template <class Type> double CArray1<Type>::GetSum() const
{
	return CArrayTools<Type>::GetSum(GetBuffer(), GetNbElements());
}

template <class Type> double CArray1<Type>::GetEnergy() const
{
	return CArrayTools<Type>::GetEnergy(GetBuffer(), GetNbElements());
}

template <class Type> double CArray1<Type>::GetEntropy() const
{
	return CArrayTools<Type>::GetEntropy(GetBuffer(), GetNbElements());
}

template <class Type> double CArray1<Type>::GetHomogeneity() const
{
	return CArrayTools<Type>::GetHomogeneity(GetBuffer(), GetNbElements());
}

template <class Type> double CArray1<Type>::GetInertia() const
{
	return CArrayTools<Type>::GetInertia(GetBuffer(), GetNbElements());
}

// various Data Processing operations
// ----------------------------------
template <class Type> void CArray1<Type>::Threshold(const long double p_ZeroToOneThershold, 
													const ThreshModeEnum p_Mode /* = LT */)
{
	Threshold(Type(GetMax()*p_ZeroToOneThershold), p_Mode);
}

template <class Type> void CArray1<Type>::Threshold(const Type p_Threshold, const ThreshModeEnum p_Mode /* = LT */)
{
	CArrayTools<Type>::Threshold(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

template <class Type> void CArray1<Type>::Threshold(const Type p_MinThreshold, const Type p_MaxThreshold,
													const ThreshModeEnum p_MinMode /* = LT */, 
													const ThreshModeEnum p_MaxMode /* = GEQ */)
{
	Threshold(p_MinThreshold, p_MinMode);
	Threshold(p_MaxThreshold, p_MaxMode);
}

template <class Type> void CArray1<Type>::Binarize(const Type p_Threshold /*= 0*/, const ThreshModeEnum p_Mode /* = GT*/)
{
	CArrayTools<Type>::Binarize(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

template <class Type> void CArray1<Type>::GetMask(CArray1<char>& p_Mask) const
{
	if(p_Mask.SetSize(GetSize()))
	{
		p_Mask.SetValue(0);
		CArrayTools<Type>::GetMask(p_Mask.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot allocate mask array");
}

template <class Type> void CArray1<Type>::GetMask(CArray1<char>& p_Mask, 
												  const long double p_ZeroToOneThershold,
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray1<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_ZeroToOneThershold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGMSG("Cannot create intermediate array");
}

template <class Type> void CArray1<Type>::GetMask(CArray1<char>& p_Mask, const Type p_Threshold, 
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray1<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_Threshold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGMSG("Cannot create intermediate array");
}

template <class Type> void CArray1<Type>::GetMask(CArray1<char>& p_Mask, const Type p_MinThreshold, 
												  const Type p_MaxThreshold, 
												  const ThreshModeEnum p_MinMode /* = LT */, 
												  const ThreshModeEnum p_MaxMode /* = GEQ */) const
{
	CArray1<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_MinThreshold, p_MaxThreshold, p_MinMode, p_MaxMode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGMSG("Cannot create intermediate array");
}

template <class Type> void CArray1<Type>::Or(const CArray1<char>& p_Mask)						
{
	if(m_Width == p_Mask.Width())
		CArrayTools<Type>::Or(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray1<Type>::And(const CArray1<char>& p_Mask)						
{
	if(m_Width == p_Mask.Width())
		CArrayTools<Type>::And(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray1<Type>::Xor(const CArray1<char>& p_Mask)						
{
	if(m_Width == p_Mask.Width())
		CArrayTools<Type>::Xor(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray1<Type>::Not()											
{
	CArrayTools<Type>::Not(GetBuffer(), GetNbElements());
}

template <class Type> void CArray1<Type>::Mask(const CArray1<char>& p_Mask)					
{
	if(m_Width == p_Mask.Width())
		CArrayTools<Type>::Mask(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

// margin cleaning
// ---------------
template <class Type> void CArray1<Type>::CleanMargins(const int p_CleanWidth /* = 1 */)
{
	if(p_CleanWidth < 0)
	{
		LOGERR("Clean Width < 0");
		return;
	}
	if(p_CleanWidth > m_Width)
	{
		LOGERR("Clean Width out of index range");
		return;
	}
	
	register int	i1, i2;
	for(i1=0, i2=m_Width-1; i1 < p_CleanWidth; i1++, i2--)
	{	m_pData[i1] = 0;
		m_pData[i2] = 0;
	}
}

// statistics operations
// ---------------------
template <class Type> bool CArray1<Type>::Normalize()
{
	Type	l_sum;
		
	if((l_sum = Type(GetSum())) == 0)
		return false;
			
	*this	/= l_sum;
	
	return true;
}

template <class Type> void CArray1<Type>::GetHistogram(CArray1<UINT>& p_Result) const
{
	if(p_Result.SetSize(int(GetMax()) + 1))
	{
		p_Result.SetValue(0);
		CArrayTools<Type>::GetHistogram(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot create result array");
}

template <class Type> bool CArray1<Type>::GetStatistics(double& p_XMean, double& p_X2Mean, double& p_XVariance, 
	const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetStatistics(GetBuffer(), GetNbElements(), p_XMean, p_X2Mean, 
				p_XVariance, p_NoZero);
}

template <class Type> double CArray1<Type>::GetCorrelation(CArray1<Type>& p_Arr) const
{
	if(!!(*this))
	{
		if(m_Width == p_Arr.Width())
			return CArrayTools<Type>::GetCorrelation(p_Arr.GetBuffer(), GetBuffer(), GetNbElements());
		else
			LOGERR("Try to compute Correlation of arrays of different size");
	}
	else
		LOGERR("object not allocated properly");

	return 0;
}

// sorting fucntion
// ----------------
template <class Type> void CArray1<Type>::Qsort(const bool p_bAscending /* = true */)
{
	CArrayTools<Type>::Qsort(GetBuffer(), GetNbElements(), p_bAscending);
}


// Explicit instanciation for several types
// ----------------------------------------
template class CArray1<int>;
template class CArray1<short>;
template class CArray1<char>;
//template class CArray1<UINT>;
template class CArray1<long>;
template class CArray1<char>;
//template class CArray1<WORD>;
template class CArray1<float>;
template class CArray1<double>;
//template class CArray1<DWORD>;
