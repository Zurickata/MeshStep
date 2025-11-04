// Array\Array2.cpp

#include "../Array/Array2.h"
#include "../Array/ArrayTools.h"
//#include "../Services/Log.h"
#include <math.h>

// intialization of static constant member
// ---------------------------------------
template <class Type> const int CArray2<Type>::DIST_FACT = 10;

// --------------
// public methods
// --------------

// constructors
// -----------
template <class Type> CArray2<Type>::CArray2(const int p_Height, const int p_Width) :
	  CContainer2<Type>(p_Height, p_Width) {}

template <class Type> CArray2<Type>::CArray2(const CSize& p_Size) :
		CContainer2<Type>(p_Size) {}

template <class Type> CArray2<Type>::CArray2(const Type* p_pSrc, const int p_Height, const int p_Width) :
		CContainer2<Type>(p_pSrc, p_Height, p_Width) {}

template <class Type> CArray2<Type>::CArray2(const CArray2<Type>& p_Src) :
		CContainer2<Type>(p_Src) {}

template <class Type> CArray2<Type>::CArray2(const CArray2<Type>& p_Src, const int p_Height, const int p_Width) :
		CContainer2<Type>(p_Src, p_Height, p_Width) {} 

template <class Type> CArray2<Type>::CArray2(const CArray2<Type>& p_Src, const CSize& p_Size) :
		CContainer2<Type>(p_Src, p_Size) {}

// desctructor
// -----------
template <class Type> CArray2<Type>::~CArray2() { }

// Addition operators
// ------------------
template <class Type> CArray2<Type> CArray2<Type>::operator+(const CArray2<Type>& p_Arr)
{
	CArray2<Type> l_res;
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

template <class Type> CArray2<Type> CArray2<Type>::operator+(const Type p_Val)
{
	CArray2<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Add(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray2<Type>& CArray2<Type>::operator+=(const CArray2<Type>& p_Arr)
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

template <class Type> const CArray2<Type>& CArray2<Type>::operator+=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Add(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subtraction operators
// ---------------------
template <class Type> CArray2<Type> CArray2<Type>::operator-(const CArray2<Type>& p_Arr)
{
	CArray2<Type> l_res;
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

template <class Type> CArray2<Type> CArray2<Type>::operator-(const Type p_Val)
{
	CArray2<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Sub(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray2<Type>& CArray2<Type>::operator-=(const CArray2<Type>& p_Arr)
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

template <class Type> const CArray2<Type>& CArray2<Type>::operator-=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Sub(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Multiplication operators
// ------------------------
template <class Type> CArray2<Type> CArray2<Type>::operator*(const CArray2<Type>& p_Arr)
{
	CArray2<Type> l_res(*this);
	
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

template <class Type> CArray2<Type> CArray2<Type>::operator*(const Type p_Val)
{
	CArray2<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Mult(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray2<Type>& CArray2<Type>::operator*=(const CArray2<Type>& p_Arr)
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

template <class Type> const CArray2<Type>& CArray2<Type>::operator*=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Mult(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// Subdivision operators
// ---------------------
template <class Type> CArray2<Type> CArray2<Type>::operator/(const CArray2<Type>& p_Arr)
{
	CArray2<Type> l_res;

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

template <class Type> CArray2<Type> CArray2<Type>::operator/(const Type p_Val)
{
	CArray2<Type> l_res(*this);

	if(!!l_res)
		CArrayTools<Type>::Div(l_res.GetBuffer(), p_Val, l_res.GetNbElements());
	else
		LOGERR("Cannot create result array");
		
	return l_res;
}

template <class Type> const CArray2<Type>& CArray2<Type>::operator/=(const CArray2<Type>& p_Arr)
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

template <class Type> const CArray2<Type>& CArray2<Type>::operator/=(const Type p_Val)
{
	if(!!(*this))
		CArrayTools<Type>::Div(GetBuffer(), p_Val, GetNbElements());
	else
		LOGERR("object not allocated properly");
	
	return *this;
}

// various operations
// ------------------
template <class Type> void CArray2<Type>::Abs()											
{
	CArrayTools<Type>::Abs(GetBuffer(), GetNbElements());
}

template <class Type> void CArray2<Type>::Sqrt(const Type p_IfLessZero /* = 0 */)											
{
	CArrayTools<Type>::Sqrt(GetBuffer(), GetNbElements(), p_IfLessZero);
}

template <class Type> void CArray2<Type>::Log10(const Type p_IfLessOrEqZero /* = 0 */)											
{
	CArrayTools<Type>::Log10(GetBuffer(), GetNbElements(), p_IfLessOrEqZero);
}

// conversion between types
// ------------------------
template <class Type> void CArray2<Type>::Convert(CArray2<char>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<BYTE>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<short>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<WORD>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<int>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<UINT>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<long>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<DWORD>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<float>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

template <class Type> void CArray2<Type>::Convert(CArray2<double>& p_Result) const
{
	if(p_Result.SetSize(m_Height, m_Width))
		::Convert(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	else
		LOGERR("Cannot create result array");
}

// various value informations
// --------------------------
template <class Type> Type CArray2<Type>::GetMin(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMin(GetBuffer(), GetNbElements(), p_NoZero);
}

template <class Type> Type CArray2<Type>::GetMinPos(int& p_PosY, int& p_PosX) const
{
	int l_pos;
	Type l_val = CArrayTools<Type>::GetMinPos(GetBuffer(), GetNbElements(), l_pos);

	p_PosY = l_pos/m_Width;
	p_PosX = l_pos%m_Width;

	return l_val;
}

template <class Type> Type CArray2<Type>::GetMinCol(const int p_Col) const
{
	return CArrayTools<Type>::GetMin(m_Width, GetBuffer() + p_Col, m_Height);
}

template <class Type> Type CArray2<Type>::GetMinLine(const int p_Line) const
{
	return CArrayTools<Type>::GetMin(&m_pData[p_Line][0], m_Width, false);
}

template <class Type> Type CArray2<Type>::GetMax(const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetMax(GetBuffer(), GetNbElements(), p_NoZero);
}

template <class Type> Type CArray2<Type>::GetMaxPos(int& p_PosY, int& p_PosX) const
{
	int l_pos;
	Type l_val = CArrayTools<Type>::GetMaxPos(GetBuffer(), GetNbElements(), l_pos);

	p_PosY = l_pos/m_Width;
	p_PosX = l_pos%m_Width;

	return l_val;
}

template <class Type> Type CArray2<Type>::GetMaxCol(const int p_Col) const
{
	return CArrayTools<Type>::GetMax(m_Width, GetBuffer() + p_Col, m_Height);
}

template <class Type> Type CArray2<Type>::GetMaxLine(const int p_Line) const
{
	return CArrayTools<Type>::GetMax(&m_pData[p_Line][0], m_Width, false);
}

template <class Type> double CArray2<Type>::GetMean() const 
{ 
	return GetSum()/GetNbElements(); 
}

template <class Type> double CArray2<Type>::GetSum() const
{
	return CArrayTools<Type>::GetSum(GetBuffer(), GetNbElements());
}

template <class Type> double CArray2<Type>::GetEnergy() const
{
	return CArrayTools<Type>::GetEnergy(GetBuffer(), GetNbElements());
}

template <class Type> double CArray2<Type>::GetEntropy() const
{
	return CArrayTools<Type>::GetEntropy(GetBuffer(), GetNbElements());
}

template <class Type> double CArray2<Type>::GetHomogeneity() const
{
	return CArrayTools<Type>::GetHomogeneity(GetBuffer(), GetNbElements());
}

template <class Type> double CArray2<Type>::GetInertia() const
{
	return CArrayTools<Type>::GetInertia(GetBuffer(), GetNbElements());
}


// various Data Processing operations
// ----------------------------------
template <class Type> void CArray2<Type>::Threshold(const long double p_ZeroToOneThershold, 
													const ThreshModeEnum p_Mode /* = LT */)
{
	Threshold(Type(GetMax()*p_ZeroToOneThershold), p_Mode);
}

template <class Type> void CArray2<Type>::Threshold(const Type p_Threshold, const ThreshModeEnum p_Mode /* = LT */)
{
	CArrayTools<Type>::Threshold(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

template <class Type> void CArray2<Type>::Threshold(const Type p_MinThreshold, const Type p_MaxThreshold,
													const ThreshModeEnum p_MinMode /* = LT */, 
													const ThreshModeEnum p_MaxMode /* = GEQ */)
{
	Threshold(p_MinThreshold, p_MinMode);
	Threshold(p_MaxThreshold, p_MaxMode);
}

template <class Type> void CArray2<Type>::Binarize(const Type p_Threshold /*= 0*/, const ThreshModeEnum p_Mode /* = GT*/)
{
	CArrayTools<Type>::Binarize(GetBuffer(), GetNbElements(), p_Threshold, p_Mode);
}

template <class Type> bool CArray2<Type>::GetBinaryObjectsLimits(int& p_OffX, int& p_TailX, 
	int& p_OffY, int& p_TailY)
{
	p_OffX	= m_Width;
	p_OffY	= m_Height;
	p_TailX	= -1;
	p_TailY	= -1;
	
	register Type* pSrc = GetBuffer(); 
	for(register int jj=0; jj < m_Height; jj++)
	{	for(register int ii=0; ii < m_Width; ii++)
		{	if(*pSrc++)
			{	if(ii < p_OffX)
					p_OffX	= ii;
				if(ii > p_TailX)
					p_TailX	= ii;
				if(jj < p_OffY)
					p_OffY	= jj;
				if(jj > p_TailY)
					p_TailY	= jj;
	}	}	}
	
	return p_TailX != -1;
}

template <class Type> void	CArray2<Type>::LabelizeConnectedObjects(CArray1<int>& p_ObSize, const Type p_Val,
				int p_OffY, int p_TailY, int p_OffX, int p_TailX)
{
	p_OffX	= max(0, p_OffX);
	p_OffY	= max(0, p_OffY);

	p_TailX	= min(p_TailX, m_Width);
	p_TailY	= min(p_TailY, m_Height);

	enum LocalDirEnum {	Center, North, East, South, West, Nowhere };
	
	if(!p_ObSize.SetSize(256))
	{
		LOGERR("Cannot allocate ObSize");
		return;
	}
	p_ObSize.SetValue(0);

	int l_StackDim = int(GetSum()) + m_Width;

	CArray1<short>	l_StackX(l_StackDim);
	if(!l_StackX)
	{
		LOGERR("Cannot create intermediate array");
		return;
	}

	CArray1<short>	l_StackY(l_StackDim);
	if(!l_StackY)
	{
		LOGERR("Cannot create intermediate array");
		return;
	}

	CArray1<BYTE>	l_StackDir(l_StackDim);
	if(!l_StackDir)
	{
		LOGERR("Cannot create intermediate array");
		return;
	}

	int			l_IndStack = -1, l_Cluster = 2;
	register	short	ii, jj;
	short		i1, j1;

	for(jj=p_OffY; jj < p_TailY; jj++)
	{	for(ii=p_OffX; ii < p_TailY; ii++)
		{	if((l_Cluster < 256) && (m_pData[jj][ii] == p_Val))
			{	l_StackX[++l_IndStack]	= ii;
				l_StackY[l_IndStack]	= jj;
				l_StackDir[l_IndStack]	= Center;
				while(l_IndStack >= 0)
				{	i1 = l_StackX[l_IndStack];
					j1 = l_StackY[l_IndStack];		
					
					if(l_StackDir[l_IndStack] == Center)
					{	if((j1 >= p_OffY) && (j1 < p_TailY) && (i1 >= p_OffX) && (i1 < p_TailX) && (m_pData[j1][i1] == p_Val))
						{	m_pData[j1][i1]		= Type(l_Cluster);
							p_ObSize[l_Cluster]++;

							l_StackDir[l_IndStack++]	= North;				
							l_StackX[l_IndStack]		= i1;
							l_StackY[l_IndStack]		= j1 - 1;
							l_StackDir[l_IndStack]		= Center;
						}
						else
							l_IndStack--;
					}
					else if(++l_StackDir[l_IndStack] < Nowhere)
					{	switch(l_StackDir[l_IndStack])
						{	case North:
								j1--;
								break;
							case East:
								i1++;
								break;
							case South:
								j1++;
								break;
							case West:
								i1--;
								break;
						}
						l_StackX[++l_IndStack]	= i1;
						l_StackY[l_IndStack]	= j1;
						l_StackDir[l_IndStack]	= Center;				
					}
					else
						l_IndStack--;
				}
				l_Cluster++;
	}	}	}
}


template <class Type> void CArray2<Type>::GetMask(CArray2<BYTE>& p_Mask) const
{
	if(p_Mask.SetSize(GetSize()))
	{
		p_Mask.SetValue(0);
		CArrayTools<Type>::GetMask(p_Mask.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot allocate mask array");
}

template <class Type> void CArray2<Type>::GetMask(CArray2<BYTE>& p_Mask, 
												  const long double p_ZeroToOneThershold,
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray2<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_ZeroToOneThershold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

template <class Type> void CArray2<Type>::GetMask(CArray2<BYTE>& p_Mask, const Type p_Threshold, 
												  const ThreshModeEnum p_Mode /* = LT */) const
{
	CArray2<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_Threshold, p_Mode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

template <class Type> void CArray2<Type>::GetMask(CArray2<BYTE>& p_Mask, const Type p_MinThreshold, 
												  const Type p_MaxThreshold, 
												  const ThreshModeEnum p_MinMode /* = LT */, 
												  const ThreshModeEnum p_MaxMode /* = GEQ */) const
{
	CArray2<Type>	l_Arr(*this);
	if(!!l_Arr)
	{
		l_Arr.Threshold(p_MinThreshold, p_MaxThreshold, p_MinMode, p_MaxMode);
		l_Arr.GetMask(p_Mask);
	}
	else
		LOGERR("Cannot create intermediate array");
}

template <class Type> void CArray2<Type>::Or(const CArray2<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height())
		CArrayTools<Type>::Or(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray2<Type>::And(const CArray2<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height())
		CArrayTools<Type>::And(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray2<Type>::Xor(const CArray2<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height())
		CArrayTools<Type>::Xor(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void CArray2<Type>::Not()											
{
	CArrayTools<Type>::Not(GetBuffer(), GetNbElements());
}

template <class Type> void CArray2<Type>::Mask(const CArray2<BYTE>& p_Mask)						
{
	if(m_Width == p_Mask.Width() && m_Height == p_Mask.Height())
		CArrayTools<Type>::Mask(GetBuffer(), p_Mask.GetBuffer(), GetNbElements());
	else
		LOGERR("try to apply binary operator on arrays of different size");
}

template <class Type> void	CArray2<Type>::FillCircle(const CPoint& p_Center, int p_Radius, Type p_Value /* =1 */)
{
	if(p_Center.x>=0 && p_Center.x<m_Width && p_Center.y>=0 && p_Center.y<m_Height)
	{
		double l_DiagLength = sqrt(m_Width*m_Width + m_Height*m_Height);
		if(p_Radius > 0)
		{
			if(p_Radius > l_DiagLength)
				SetValue(p_Value);
			else
			{
				for(register int j=0; j<m_Height; j++)
				{
					double l_Y = p_Center.y-j;
					l_Y *= l_Y;
					for(register int i=0; i<m_Width; i++)
					{
						double l_X = p_Center.x-i;
						double l_Dist = sqrt(l_X*l_X + l_Y);
						if(l_Dist <= p_Radius)
							m_pData[j][i] = p_Value;
					}
				}
			}
		}
		else
			LOGMSG("Negative or null radius");
	}
	else
		LOGERR("Center coordinates out of range");

}

// margin cleaning
// ---------------
template <class Type> void CArray2<Type>::CleanMargins(const int p_CleanWidth /* = 1 */)
{
	if(p_CleanWidth < 0)
	{
		LOGERR("Clean Width  < 0");
		return;
	}
	if(p_CleanWidth > m_Height || p_CleanWidth > m_Width)
	{
		LOGERR("CleanWidth out of index range");
		return;
	}

	register int	i1, i2, jj;
	int	 l_limY = m_Height - p_CleanWidth;
	
	for(jj=0; jj < p_CleanWidth; jj++)
		memset(&m_pData[jj][0], 0, m_Width*sizeof(Type));
	
	for(; jj < l_limY; jj++)
	{	for(i1=0, i2=m_Width-1; i1 < p_CleanWidth; i1++, i2--)
		{	m_pData[jj][i1] = 0;
			m_pData[jj][i2] = 0;
	}	}
		
	for(; jj < m_Height; jj++)
		memset(&m_pData[jj][0], 0, m_Width*sizeof(Type));
}


// statistics operations
// ---------------------
template <class Type> bool CArray2<Type>::Normalize()
{
	Type	l_sum;
		
	if((l_sum = Type(GetSum())) == 0)
		return false;
			
	*this	/= l_sum;
	
	return true;
}

template <class Type> void CArray2<Type>::GetHistogram(CArray1<UINT>& p_Result) const
{
	if(p_Result.SetSize(int(GetMax()) + 1))
	{
		p_Result.SetValue(0);
		CArrayTools<Type>::GetHistogram(p_Result.GetBuffer(), GetBuffer(), GetNbElements());
	}
	else
		LOGERR("Cannot allocate result array");
}

template <class Type> int CArray2<Type>::GetHistogramMode() const
{
	CArray1<UINT> histo;
	GetHistogram(histo);

	if(!histo)
	{
		LOGMSG("Cannot create histogram array");
		return 0;
	}
	
	register int ii, dim = histo.Width();
	
	UINT mx	= histo.GetMax();
	for(ii=0; ii < dim; ii++)
		if(histo[ii] == mx)
			break;
			
	return ii;
}

template <class Type> int CArray2<Type>::GetHistogramMin(const bool p_bWithoutZero /* = true */) const
{
	CArray1<UINT> histo;
	GetHistogram(histo);

	if(!histo)
	{
		LOGMSG("Cannot create histogram array");
		return 0;
	}
	
	register int ii, dim = histo.Width();
	
	for(ii=(p_bWithoutZero == true) ? 1 : 0; ii < dim; ii++)
		if(histo[ii] != 0)
			break;

	return (ii == dim) ? 0 : ii;
}

template <class Type> int CArray2<Type>::GetHistogramMax() const
{
	CArray1<UINT> histo;
	GetHistogram(histo);

	if(!histo)
	{
		LOGMSG("Cannot create histogram array");
		return 0;
	}
	
	register int ii, dim = histo.Width();
	
	for(ii=dim-1; ii >= 0; ii--)
		if(histo[ii] != 0)
			break;
			
	return (ii < 0) ? 0 : ii;
}

template <class Type> bool CArray2<Type>::GetStatistics(double& p_XMean, double& p_X2Mean, double& p_XVariance, 
	const bool p_NoZero /* = false */) const
{
	return CArrayTools<Type>::GetStatistics(GetBuffer(), GetNbElements(), p_XMean, p_X2Mean, 
				p_XVariance, p_NoZero);
}

template <class Type> double CArray2<Type>::GetCorrelation(CArray2<Type>& p_Arr) const
{
	if(!!(*this))
	{
		if(m_Width == p_Arr.Width() && m_Height == p_Arr.Height())
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
template <class Type> void CArray2<Type>::Qsort(const bool bAscending /* = true */)
{
	CArrayTools<Type>::Qsort(GetBuffer(), GetNbElements(), bAscending);
}

// Shift elements
// --------------
template <class Type> void CArray2<Type>::Shift(const int p_OffX, const int p_OffY)
{
	int	l_OXs, l_OYs, l_OXd, l_OYd, l_DimX, l_DimY;
	
	CArray2<Type>	l_Dest(m_Height, m_Width);
	l_Dest.SetValue(0);
	
	if((p_OffX == 0) && (p_OffY == 0))
		return;

	if((abs(p_OffX) >= m_Width) || (abs(p_OffY) >= m_Height))
	{
		LOGERR("Offset indices out of range");
		return;
	}
		
	l_DimX = m_Width - abs(p_OffX);
	l_DimY = m_Height - abs(p_OffY);
	
	if(p_OffX < 0)
	{	if(p_OffY < 0)
		{	l_OXs = -p_OffX;
			l_OXd = 0;
			l_OYs = -p_OffY;
			l_OYd = 0;
		}
		else
		{	l_OXs = -p_OffX;
			l_OXd = 0;
			l_OYs = 0;
			l_OYd = p_OffY;
	}	}
	else
	{	if(p_OffY < 0)
		{	l_OXs = 0;
			l_OXd = p_OffX;
			l_OYs = -p_OffY;
			l_OYd = 0;
		}
		else
		{	l_OXs = 0;
			l_OXd = p_OffX;
			l_OYs = 0;
			l_OYd = p_OffY;
	}	}
	
	if(!!l_Dest)
	{
		for(int register ii=0; ii < l_DimY; ii++)
			memcpy(&l_Dest[l_OYd+ii][l_OXd], &m_pData[l_OYs+ii][l_OXs], l_DimX*sizeof(Type));	
		*this = l_Dest;
	}
	else
		LOGERR("cannot create intermediate array");
}

template <class Type> void CArray2<Type>::Shift(const CPoint& p_Off)
{
	Shift(p_Off.x, p_Off.y); 
}

// transposition
// -------------
template <class Type> void CArray2<Type>::Transpose()
{
	CArray2<Type> l_Arr(m_Width, m_Height);
	
	if(!!l_Arr)
	{
		for(register int jj=0; jj < m_Height; jj++)
			for(register int ii=0; ii < m_Width; ii++)
				l_Arr[ii][jj] = m_pData[jj][ii];		
		*this = l_Arr;
	}
	else
		LOGERR("cannot create intermediate array");
}

// flip in X direction
// -------------------
template <class Type> void CArray2<Type>::ReflexionX()
{	
	register int ii, jj, i1;
	int	l_Dim = m_Width/2;
	
	for(jj=0; jj < m_Height; jj++)
	{	for(ii=0, i1=m_Width-1; ii < l_Dim; ii++, i1--)
		{	Type l_Val = m_pData[jj][i1];
			m_pData[jj][i1] = m_pData[jj][ii];
			m_pData[jj][ii] = l_Val;
	}	}
}

// flip in X direction
// -------------------
template <class Type> void CArray2<Type>::ReflexionY()
{
	CArray1<Type> l_Arr(m_Width);
	
	register int ii, jj;
	int	l_Dim = m_Height/2;
	if(!!l_Arr)
		for(jj=0, ii=m_Height-1; jj < l_Dim; jj++, ii--)
		{	memcpy(&l_Arr[0], &m_pData[jj][0], l_Arr.Sizeof());
			memcpy(&m_pData[jj][0], &m_pData[ii][0], l_Arr.Sizeof());
			memcpy(&m_pData[ii][0], &l_Arr[0], l_Arr.Sizeof());
		}
	else
		LOGERR("cannot create intermediate array");
}

// flip around the center
// ----------------------
template <class Type> void CArray2<Type>::ReflexionCenter()
{
	CArray2<Type> l_Arr(m_Height, m_Width);
	
	register int ii, jj, i1, j1;
	if(!!l_Arr)
	{
		for(jj=0, j1=m_Height-1; jj < m_Height; jj++, j1--)
			for(ii=0, i1=m_Width-1; ii < m_Width; ii++, i1--)
				l_Arr[j1][i1] = m_pData[jj][ii];
		*this = l_Arr;
	}
	else
		LOGERR("cannot create intermediate array");
}


// Binary objects operations
// -------------------------
template <class Type> void CArray2<Type>::SetConnection(const ConnectModeEnum p_Connect /* = Connect4 */)
{
	switch(p_Connect)
	{	case Connect4:
			{	int l_LimX = m_Width - 1;
				for(register int jj=1; jj < m_Height; jj++)
					for(register int ii=1; ii < l_LimX; ii++)
						if(	m_pData[jj][ii] && (m_pData[jj-1][ii] == 0) &&
							((m_pData[jj-1][ii-1] && (m_pData[jj][ii-1] == 0)) || (m_pData[jj-1][ii+1] && (m_pData[jj][ii+1] == 0))))
							m_pData[jj-1][ii] = 1;
			}
			break;
		case Connect8:
			{	int l_LimX = m_Width - 1;
				for(register int jj=1; jj < m_Height; jj++)
				{	for(register int ii=1; ii < l_LimX; ii++)
					{	if(m_pData[jj][ii] && m_pData[jj-1][ii] && (m_pData[jj-1][ii-1] || m_pData[jj-1][ii+1]))
							m_pData[jj-1][ii] = 0;
			}	}	}
			break;
	}
}

template <class Type> void CArray2<Type>::ZeroCross(const ConnectModeEnum p_Connect /* = Connect8 */,
	const DirEnum p_Dir /* = allDir */)
{
	register int	jj, ii;
	int				height=m_Height-1, width=m_Width-1;

	CArray2<Type> src(*this);
	if(!src)
	{
		LOGERR("Cannot create intermediate array");
		return;
	}

	switch(p_Dir)
	{	case AllDir:
			if(p_Connect == Connect4)
			{	for(jj=1; jj < height; jj++)
				{	for(ii=1; ii < width; ii++)
					{	if(	src[jj][ii] && src[jj][ii-1] && src[jj][ii+1] &&
							src[jj-1][ii-1] && src[jj-1][ii] && src[jj-1][ii+1] &&
							src[jj+1][ii-1] && src[jj+1][ii] && src[jj+1][ii+1])
							m_pData[jj][ii] = 0;
			}	}	}
			else
			{	for(jj=1; jj < height; jj++)
				{	for(ii=1; ii < width; ii++)
					{	if(	src[jj][ii] && src[jj][ii-1] && src[jj][ii+1] &&
							src[jj-1][ii] && src[jj+1][ii])
							m_pData[jj][ii] = 0;
			}	}	}
			break;
		case North:
			for(ii=0; ii < m_Width; ii++)
			{	for(jj=0; jj < height; jj++)
				{	if((src[jj][ii] != 0) && ((jj == 0) || (src[jj-1][ii] == 0)))
					{	for(jj++; jj <= height; jj++)
						{	if(src[jj][ii])
								m_pData[jj][ii] = 0;
							else
								break;
			}	}	}	}
			break;
		case South:
			for(ii=0; ii < m_Width; ii++)
			{	for(jj=height; jj >= 0; jj--)
				{	if((src[jj][ii] != 0) && ((jj == height) || (src[jj+1][ii] == 0)))
					{	for(jj--; jj >= 0; jj--)
						{	if(src[jj][ii])
								m_pData[jj][ii] = 0;
							else
								break;
			}	}	}	}
			break;
	}
	
	if((p_Connect == Connect4) && (p_Dir != AllDir))
		SetConnection(Connect4);
}


template <class Type> void CArray2<Type>::SetSubArray(const int p_X1, const int p_Y1, const int p_X2, const int p_Y2)
{
	SetSubArray(CPoint(p_X1, p_Y1), CSize(p_X2 - p_X1 + 1, p_Y2 - p_Y1 + 1));
}

template <class Type> void CArray2<Type>::SetSubArray(const CPoint& p_Offset, const CSize& p_Size)
{
	if(p_Offset.x < 0 || p_Offset.x >= m_Width || p_Offset.y < 0 || p_Offset.y >= m_Height)
	{
		LOGERR("Offset indices out of range");
		return;
	}
	if((p_Offset.x+p_Size.cx) > m_Width || (p_Offset.y+p_Size.cy) > m_Height)
	{
		LOGERR("Last indices will be out of range");
		return;
	}
	
	CArray2<Type>	dest(p_Size.cy, p_Size.cx);	
	dest.SetValue(0);
	if(!dest)
	{
		LOGERR("cannot create intermediate array");
		return;
	}

	for(register int jj=0; jj < p_Size.cy; jj++)
		memcpy(&dest[jj][0], &m_pData[jj+p_Offset.y][p_Offset.x], p_Size.cx*sizeof(Type));
		
	*this = dest;	
}

template <class Type> void CArray2<Type>::SetSubArray(const CPoint& p_Offset, const CPoint& p_Tail)
{
	SetSubArray(p_Offset, p_Tail - p_Offset);
}

template <class Type> void CArray2<Type>::GetSubArray(const int p_X1, const int p_Y1, const int p_X2, const int p_Y2, 
				CArray2<Type>& p_Dest)
{
	GetSubArray(CPoint(p_X1, p_Y1), CSize(p_X2 - p_X1+1, p_Y2 - p_Y1+1), p_Dest);
}

template <class Type> void CArray2<Type>::GetSubArray(const CPoint& p_Offset, const CSize& p_Size, CArray2<Type>& p_Dest)
{
	if(p_Offset.x < 0 || p_Offset.x >= m_Width || p_Offset.y < 0 || p_Offset.y >= m_Height)
	{
		LOGERR("Offset indices out of range");
		return;
	}
	if((p_Offset.x+p_Size.cx) > m_Width || (p_Offset.y+p_Size.cy) > m_Height)
	{
		LOGERR("Last indices will be out of range");
		return;
	}

	if(p_Dest.SetSize(p_Size.cy, p_Size.cx))
	{	
		p_Dest.SetValue(0);
		for(register int jj=0; jj < p_Size.cy; jj++)
			memcpy(&p_Dest[jj][0], &m_pData[jj+p_Offset.y][p_Offset.x], p_Size.cx*sizeof(Type));
	}
	else
		LOGERR("cannot allocate result array");
}

template <class Type> void CArray2<Type>::GetSubArray(const CPoint& p_Offset, const CPoint& p_Tail, CArray2<Type>& p_Dest)
{	
	GetSubArray(p_Offset, p_Tail - p_Offset, p_Dest);	
}

// distance map
// ------------
template <class Type> bool	CArray2<Type>::GetDistanceMap(CArray2<short>& p_Dist) const
{
	register int ii, jj;

	p_Dist.SetSize(GetSize());
	if(!p_Dist)
	{
		LOGERR("cannot allocate result array");
		return false;
	}
	p_Dist.SetValue(0);
		
	const int DIST_0 = 0;
	const int DIST_0_5 = int(DIST_FACT*0.5);
	const int DIST_1_0 = int(DIST_FACT*1.0);
	const int DIST_1_4 = int(DIST_FACT*1.4);
	const int DIST_1_7 = int(DIST_FACT*1.7);
	const int DIST_2_0 = int(DIST_FACT*2.0);
	const short DIST_MIN = (SHRT_MIN + 20*DIST_2_0);
	const short DIST_MAX = (SHRT_MAX - 20*DIST_2_0);

	int	limX = m_Width-1, limY = m_Height-1;

	// initialisation	
	for(jj=0; jj < m_Height; jj++)
		for(ii=0; ii < m_Width; ii++)
			p_Dist[jj][ii] = (m_pData[jj][ii] > 0) ? DIST_MAX : DIST_MIN;
	 
	//frontier corection
	for(jj=1; jj < limY; jj++)
	{	for(ii=1; ii < limX; ii++)
		{	if(m_pData[jj][ii] > 0)
			{	if(m_pData[jj-1][ii] == 0)
				{	p_Dist[jj-1][ii]	= -DIST_0_5;
					p_Dist[jj][ii]	= DIST_0_5;
				}
				else if(m_pData[jj+1][ii] == 0)
				{	p_Dist[jj+1][ii]	= -DIST_0_5;
					p_Dist[jj][ii]	= DIST_0_5;
				}
				else if(m_pData[jj][ii-1] == 0)
				{	p_Dist[jj][ii-1]	= -DIST_0_5;
					p_Dist[jj][ii]	= DIST_0_5;
				}
				else if(m_pData[jj][ii+1] == 0)
				{	p_Dist[jj][ii+1]	= -DIST_0_5;
					p_Dist[jj][ii]	= DIST_0_5;
	}	}	}	}
	
	//forward chamfering
	for(jj=0; jj < m_Height; jj++)
	{	for(ii=0; ii < m_Width; ii++)
		{	if(p_Dist[jj][ii] == DIST_0_5)
				continue;
			else if(p_Dist[jj][ii] == -DIST_0_5)
				continue;

			if(ii == 0)
			{	if(jj != 0)
				{	if(p_Dist[jj][ii] > 0)
						p_Dist[jj][ii] = min(min(p_Dist[jj][ii], p_Dist[jj-1][ii] + DIST_1_0), p_Dist[jj-1][ii+1] + DIST_1_4);
					else
						p_Dist[jj][ii] = max(max(p_Dist[jj][ii], p_Dist[jj-1][ii] - DIST_1_0), p_Dist[jj-1][ii+1] - DIST_1_4);						
			}	}
			else if((ii == limX) || (jj == 0))
			{	if(jj == 0)
				{	if(p_Dist[jj][ii] > 0)
						p_Dist[jj][ii] = min(p_Dist[jj][ii], p_Dist[jj][ii-1] + DIST_1_0);
					else
						p_Dist[jj][ii] = max(p_Dist[jj][ii], p_Dist[jj][ii-1] - DIST_1_0);		
				}	
				else
				{	if(p_Dist[jj][ii] > 0)
					{	short val		= min(min(p_Dist[jj][ii], p_Dist[jj][ii-1] + DIST_1_0), p_Dist[jj-1][ii] + DIST_1_0);
						p_Dist[jj][ii]	= min(val, p_Dist[jj-1][ii-1] + DIST_1_4);
					}
					else
					{	short val		= max(max(p_Dist[jj][ii], p_Dist[jj][ii-1] - DIST_1_0), p_Dist[jj-1][ii] - DIST_1_0);
						p_Dist[jj][ii]	= max(val, p_Dist[jj-1][ii-1] - DIST_1_4);
					
			}	}	}
			else
			{	if(p_Dist[jj][ii] > 0)
				{	short val		= min(min(p_Dist[jj][ii], p_Dist[jj][ii-1] + DIST_1_0), p_Dist[jj-1][ii] + DIST_1_0);
					p_Dist[jj][ii]	= min(min(val, p_Dist[jj-1][ii-1] + DIST_1_4), p_Dist[jj-1][ii+1] + DIST_1_4);
				}
				else
				{	short val		= max(max(p_Dist[jj][ii], p_Dist[jj][ii-1] - DIST_1_0), p_Dist[jj-1][ii] - DIST_1_0);
					p_Dist[jj][ii]	= max(max(val, p_Dist[jj-1][ii-1] - DIST_1_4), p_Dist[jj-1][ii+1] - DIST_1_4);
				
						
	}	}	}	}

	//backward chamfering
	for(jj=limY; jj >= 0; jj--)
	{	for(ii=limX; ii >= 0; ii--)
		{	if(p_Dist[jj][ii] == DIST_0_5)
				continue;
			else if(p_Dist[jj][ii] == -DIST_0_5)	
				continue;

			if(ii == limX)
			{	if(jj != limY)
				{	if(p_Dist[jj][ii] > 0)
						p_Dist[jj][ii] = min(min(p_Dist[jj][ii], p_Dist[jj+1][ii] + DIST_1_0), p_Dist[jj+1][ii-1] + DIST_1_4);
					else
						p_Dist[jj][ii] = max(max(p_Dist[jj][ii], p_Dist[jj+1][ii] - DIST_1_0), p_Dist[jj+1][ii-1] - DIST_1_4);	
			}	}	
			else if((ii == 0) || (jj == limY))
			{	if(jj == limY)
				{	if(p_Dist[jj][ii] > 0)
						p_Dist[jj][ii] = min(p_Dist[jj][ii], p_Dist[jj][ii+1] + DIST_1_0);
					else
						p_Dist[jj][ii] = max(p_Dist[jj][ii], p_Dist[jj][ii+1] - DIST_1_0);	
				}
				else
				{	if(p_Dist[jj][ii] > 0)
					{	short val		= min(min(p_Dist[jj][ii], p_Dist[jj][ii+1] + DIST_1_0), p_Dist[jj+1][ii] + DIST_1_0);
						p_Dist[jj][ii]	= min(val, p_Dist[jj+1][ii+1] + DIST_1_4);
					}
					else
					{	short val		= max(max(p_Dist[jj][ii], p_Dist[jj][ii+1] - DIST_1_0), p_Dist[jj+1][ii] - DIST_1_0);
						p_Dist[jj][ii]	= max(val, p_Dist[jj+1][ii+1] - DIST_1_4);
			}	}	}	
			else
			{	if(p_Dist[jj][ii] > 0)
				{	short val		= min(min(p_Dist[jj][ii], p_Dist[jj][ii+1] + DIST_1_0), p_Dist[jj+1][ii] + DIST_1_0);
					p_Dist[jj][ii]	= min(min(val, p_Dist[jj+1][ii-1] + DIST_1_4), p_Dist[jj+1][ii+1] + DIST_1_4);
				}
				else
				{	short val		= max(max(p_Dist[jj][ii], p_Dist[jj][ii+1] - DIST_1_0), p_Dist[jj+1][ii] - DIST_1_0);
					p_Dist[jj][ii]	= max(max(val, p_Dist[jj+1][ii-1] - DIST_1_4), p_Dist[jj+1][ii+1] - DIST_1_4);
								
	}	}	}	}	
	
	return true;
}


// Numerical recipies compatibility
// --------------------------------
template <class Type> Type** CArray2<Type>::EnableRecipies()
{
	for(register int jj=0; jj < m_Height; jj++)
		m_pData[jj]--;

	return m_pData - 1;
}

template <class Type> Type** CArray2<Type>::DisableRecipies()
{
	for(register int jj=0; jj < m_Height; jj++)
		m_pData[jj]++;

	return m_pData + 1;
}


// Explicit instanciation for several types
// ----------------------------------------
template class CArray2<int>;
template class CArray2<short>;
template class CArray2<BYTE>;
template class CArray2<UINT>;
template class CArray2<long>;
template class CArray2<char>;
template class CArray2<WORD>;
template class CArray2<float>;
template class CArray2<double>;
template class CArray2<DWORD>;
